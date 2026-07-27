# OpenObserve Python SDK

Instalação:

```bash
pip install -r requirements.txt
```

Uso:

```python
from openobserve import OpenObserve

logger = OpenObserve(
    api_url="https://logs.muvysystem.com.br/api",
    token="TOKEN",
    application="customer-platform",
    service="backend"
)

logger.info("Servidor iniciado")
```