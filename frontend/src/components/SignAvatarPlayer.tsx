import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, useAnimations, useGLTF } from '@react-three/drei'
import { Suspense, useEffect, useMemo, useRef } from 'react'
import * as THREE from 'three'
import type { SignToken } from '../api/types'
import {
  clipPreferencesForSign,
  findActionKey,
  idleActionPreferences,
} from '../lib/signAvatarMapping'

type Props = {
  signs: SignToken[]
  modelUrl?: string
  onStepChange?: (index: number) => void
}

function firstAvailableActionKey(actions: Record<string, THREE.AnimationAction | null>): string | undefined {
  return Object.keys(actions).find((key) => actions[key] != null)
}

function AvatarModel({
  signs,
  modelUrl,
  onStepChange,
}: {
  signs: SignToken[]
  modelUrl: string
  onStepChange?: (index: number) => void
}) {
  const group = useRef<THREE.Group>(null)
  const gltf = useGLTF(modelUrl)
  const scene = useMemo(() => gltf.scene.clone(), [gltf.scene])
  const { actions, mixer } = useAnimations(gltf.animations, group)

  const signsKey = useMemo(() => signs.map((s) => s.animation_id).join('|'), [signs])

  useFrame((_, delta) => {
    mixer.update(delta)
  })

  useEffect(() => {
    if (!signs.length) {
      return
    }

    let cancelled = false
    let previous: THREE.AnimationAction | null = null

    const stopAll = () => {
      Object.values(actions).forEach((action) => {
        action?.stop()
      })
    }

    const resolveActionKey = (sign: SignToken): string | undefined => {
      const prefs = clipPreferencesForSign(sign)
      const direct = findActionKey(actions, prefs)
      if (direct) {
        return direct
      }
      const idle = findActionKey(actions, idleActionPreferences())
      if (idle) {
        if (import.meta.env.DEV) {
          // eslint-disable-next-line no-console
          console.debug('[SignAvatar] missing clip for', sign.animation_id, 'prefs=', prefs, '-> Idle')
        }
        return idle
      }
      const any = firstAvailableActionKey(actions)
      if (import.meta.env.DEV && any) {
        // eslint-disable-next-line no-console
        console.debug('[SignAvatar] no Idle; using first action', any, 'for', sign.animation_id)
      }
      return any
    }

    const playSequence = async () => {
      stopAll()
      for (let i = 0; i < signs.length; i += 1) {
        if (cancelled) {
          return
        }
        onStepChange?.(i)
        const sign = signs[i]
        const actionKey = resolveActionKey(sign)
        if (!actionKey) {
          break
        }
        const next = actions[actionKey]
        if (!next) {
          break
        }
        previous?.fadeOut(0.25)
        next.reset().fadeIn(0.25).play()
        previous = next

        const clipDuration = next.getClip().duration
        const clipMs = clipDuration * 1000
        const requested = sign.duration_ms ?? 800
        const waitMs = Math.min(4500, Math.max(clipMs * 0.9, requested))
        await new Promise<void>((resolve) => {
          setTimeout(resolve, waitMs)
        })
      }
      if (!cancelled) {
        onStepChange?.(-1)
        previous?.fadeOut(0.35)
        const idleKey = findActionKey(actions, idleActionPreferences()) ?? firstAvailableActionKey(actions)
        const idle = idleKey ? actions[idleKey] : null
        idle?.reset().fadeIn(0.35).play()
      }
    }

    void playSequence()

    return () => {
      cancelled = true
      stopAll()
    }
  }, [signs, signsKey, actions, mixer, onStepChange])

  return (
    <group ref={group} dispose={null}>
      <primitive object={scene} scale={0.9} position={[0, -1.1, 0]} />
    </group>
  )
}

function Loader() {
  return (
    <mesh>
      <boxGeometry args={[0.35, 0.35, 0.35]} />
      <meshStandardMaterial color="#7c93ee" />
    </mesh>
  )
}

export function SignAvatarPlayer({ signs, modelUrl = '/avatars/placeholder.glb', onStepChange }: Props) {
  useEffect(() => {
    void useGLTF.preload(modelUrl)
  }, [modelUrl])

  if (!signs.length) {
    return (
      <div className="avatar-panel avatar-panel--empty">
        <p>El avatar reproducirá la secuencia cuando traduzcas un texto.</p>
      </div>
    )
  }

  return (
    <div className="avatar-panel">
      <Canvas
        className="avatar-canvas"
        camera={{ position: [0, 1.4, 3.2], fov: 40 }}
        dpr={[1, 2]}
      >
        <color attach="background" args={['#eef1fb']} />
        <ambientLight intensity={0.65} />
        <directionalLight position={[3, 4, 2]} intensity={1.1} />
        <Suspense fallback={<Loader />}>
          <AvatarModel signs={signs} modelUrl={modelUrl} onStepChange={onStepChange} />
        </Suspense>
        <OrbitControls enablePan={false} minDistance={2} maxDistance={5} target={[0, 0.9, 0]} />
      </Canvas>
    </div>
  )
}
