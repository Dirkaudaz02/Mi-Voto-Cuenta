# Revisor de versiones

La ejecución automática está en GitHub Actions: **Control de calidad 9.5**.

- Evalúa criterios estáticos verificables de código y de política de datos.
- Rechaza (exit 1) si cualquiera de las áreas queda bajo 9.5/10.
- No representa un agente de IA autónomo ni una auditoría independiente.
- Las comprobaciones son preliminares: no prueban que los datos periodísticos sean verdaderos ni que el sitio esté libre de vulnerabilidades.
- Para impedir merges directos, configurar en GitHub **Settings → Rules → Rulesets** la protección de `main` con el check requerido `revisar` y pull requests obligatorios.
- Si GitHub Pages publica directamente desde `main`, los push directos pueden publicar sin esperar al workflow. Se recomienda publicar mediante despliegue condicionado al éxito del control.
