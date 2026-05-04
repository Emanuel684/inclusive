# Frontend - Inclusive

SPA en React + Vite con 3 flujos:

- Texto a señas (con avatar 3D y secuencia de chips)
- Imagen a señas
- Video de señas a texto

## Comandos

```bash
npm install
npm run dev
npm run build
```

## Configuración

Variable opcional:

- `VITE_API_BASE_URL` (default: `http://localhost:8000`)

## Rutas

- `/text-to-sign`
- `/image-to-sign`
- `/video-sign-to-text`

## Avatar y animaciones (`text-to-sign`)

- Modelo GLB: `public/avatars/placeholder.glb` (Vite lo copia a `dist/avatars/`).
- Mapeo `animation_id` del backend → preferencias de clips del GLB: [`src/lib/signAvatarMapping.ts`](src/lib/signAvatarMapping.ts).
- Política **best effort**: si no hay clip para un `animation_id`, se intenta `Idle` y en último caso la primera acción disponible del modelo (solo en desarrollo se registra `console.debug`).

### Añadir un gloss del diccionario

1. En backend, el token del diccionario produce `animation_id` tipo `lex_<slug>` con `slug` en minúsculas (ej. `lex_hola`).
2. En frontend, añade una entrada en `LEX_CLIP_BY_SLUG` con la lista ordenada de nombres de clip **base** (`Wave`, `ThumbsUp`, …). Los nombres reales del GLB pueden incluir prefijo (`RobotArmature|Wave`); `findActionKey` hace coincidencia flexible.

### Añadir deletreo

- Cada letra usa `spell_<letra>` en minúsculas (`spell_a`). La rotación de gestos por letra está en `spellLetterPreferences`.

## Docker

```bash
docker build -t inclusive-frontend ./frontend
docker run --rm -p 5173:80 inclusive-frontend
```

## Checklist visual rápido

- Texto: layout 2 columnas desde ~1024px; avatar no debe tapar el textarea en móvil.
- Imagen / video: bloque de resultado con `result-block`, sin `card` anidado.
- Estado de carga: badge distinto de los chips de resultado.
