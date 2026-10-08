# Mermaid minimal patterns (own notes, not copied docs)

## Flowchart
```mermaid
flowchart TD
  A[Client] -->|token| B[Auth]
  B --> C[API]
```

## Sequence
```mermaid
sequenceDiagram
  participant C as Client
  participant S as Server
  C->>S: GET /token
  S-->>C: 200 OK
```

## Failure modes to avoid
- `--<` is never valid. Use `-->`.
- `A --|label| B` needs full edge: `A -->|label| B`.
- Quote labels with commas/colons: `A["a, b: c"]`.
- Keep IDs stable: A, B, C. Labels can change, IDs must not drift.
- One name per thing: do not mix worker/agent/executor.

Full API: `mermaid.parse(text)` validates without rendering.
