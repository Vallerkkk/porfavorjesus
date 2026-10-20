# Órbita — Guia de Configuração 100% Gratuita (`C:\Users\João Pedro\Desktop\SITEEE`)

Este pacote contém todos os arquivos prontos para você extrair diretamente na sua pasta:
`C:\Users\João Pedro\Desktop\SITEEE`

## Arquivos Inclusos
- `orbita.html` / `index.html`: Front-end completo atualizado com WebRTC real (câmera e compartilhamento de tela via navegador), agrupamento de mensagens, autocomplete de `@menções` e `#canais`, upload de imagens (`Ctrl+V` ou botão `+`), sincronização multi-abas (`BroadcastChannel`) e cliente WebSocket.
- `server.py`: Servidor back-end em Python (FastAPI) com WebSockets em tempo real, banco de dados **SQLite** gratuito (`orbita.db`) e gerador de token JWT `/token` para o LiveKit Cloud Free.
- `iniciar_orbita.bat`: Script automático para Windows — basta dar **duplo-clique** para criar a `.venv`, instalar as dependências gratuitas e abrir `http://localhost:8000`.
- `render.yaml`: Configuração pronta para hospedar gratuitamente na nuvem.

## Passo 1 — Rodar no seu PC agora mesmo (Custo Zero)
1. Extraia todos os arquivos deste `.zip` dentro de `C:\Users\João Pedro\Desktop\SITEEE`.
2. Dê **duplo-clique** em `iniciar_orbita.bat` (ou abra o PowerShell na pasta e execute `.\iniciar_orbita.bat`).
3. O site abrirá automaticamente em `http://localhost:8000` com o selo verde **Servidor Ativo** no topo!

## Passo 2 — Publicar na Internet 100% de Graça
- **Opção A — Apenas Front-end Estático + P2P (Cloudflare Pages)**:
  1. Acesse https://pages.cloudflare.com/ (plano Free ilimitado para arquivos estáticos).
  2. Arraste a pasta `SITEEE` em **Upload Assets** e publique em segundos com HTTPS gratuito.
- **Opção B — Servidor Completo Python + WebSockets (Render Free)**:
  1. Suba a pasta `SITEEE` em um repositório gratuito no GitHub.
  2. No https://render.com/ crie um novo **Web Service** escolhendo o plano **Free ($0/mês)**.
  3. No botão **Configurar Grátis** no topo do Órbita, troque a URL WebSocket para `wss://seu-app.onrender.com/ws`.
- **Opção C — Voz e Vídeo Global (LiveKit Cloud Build Plan - $0/mês)**:
  1. Crie uma conta gratuita sem cartão em https://cloud.livekit.io/ (plano **Build** gratuito com até 7.500 minutos/50GB mensais).
  2. Copie sua `LIVEKIT_URL`, `LIVEKIT_API_KEY` e `LIVEKIT_API_SECRET` nas variáveis de ambiente do `server.py`.
