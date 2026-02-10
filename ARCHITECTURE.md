# PALCO ZERO - ARQUITETURA
## Estrutura técnica e State Machine

---

## VISÃO GERAL

O Palco Zero é uma experiência web premium de AR cross-platform construída com:
- **HTML/CSS/JS puro** (sem frameworks pesados)
- **model-viewer** para renderização 3D e AR
- **State Machine** para gerenciamento de estados
- **Arquitetura modular** para escalabilidade

---

## ESTRUTURA DE ARQUIVOS

```
palco-zero/
├── index.html                    # HTML principal
├── styles-premium.css            # Estilos premium com glassmorphism
├── state-machine.js              # Gerenciador de estados
├── ar-manager.js                 # Lógica de AR e validação
├── photo-mode.js                 # Modo foto (opcional)
├── app.js                        # Orquestrador principal
└── models/
    ├── product.glb               # Modelo 3D (Android + web)
    └── product.usdz              # Modelo AR (iOS Quick Look)
```

---

## STATE MACHINE

### Estados Disponíveis

```
idle ──────► loading ──────► ready ──────► ar
                │                │          │
                │                ▼          │
                └─────────► photo ◄─────────┘
```

#### 1. **idle**
- **Descrição:** Estado inicial, antes de qualquer carregamento
- **UI:** Nada renderizado ainda
- **Transições possíveis:** → `loading`

#### 2. **loading**
- **Descrição:** Modelo 3D está carregando
- **UI:** Loading skeleton + texto "Preparando experiência..."
- **Progress bar:** Atualizada conforme modelo carrega
- **Transições possíveis:** → `ready`, → `idle` (erro)

#### 3. **ready**
- **Descrição:** Modelo carregado, experiência pronta
- **UI:** Modelo 3D visível + cards de conteúdo + botão AR (se suportado)
- **Interação:** Usuário pode rotacionar modelo, ver instruções
- **Transições possíveis:** → `ar`, → `photo`, → `loading` (reload)

#### 4. **ar**
- **Descrição:** Sessão AR ativa (Quick Look ou Scene Viewer)
- **UI:** Indicador de status AR no canto superior direito
- **Tracking:** Eventos `ar-status` sendo monitorados
- **Transições possíveis:** → `ready` (sair do AR)

#### 5. **photo**
- **Descrição:** Modo foto ativo (captura de ambiente)
- **UI:** Stream de câmera + controles de captura
- **Opcional:** Pode ter foto já capturada como background
- **Transições possíveis:** → `ready` (cancelar/sair)

### Transições Inválidas

O state machine **bloqueia** transições inválidas:
- `idle` não pode ir direto para `ar`
- `loading` não pode ir direto para `photo`
- `ar` não pode ir direto para `photo`

Isso previne bugs e garante fluxo consistente.

---

## COMPONENTES PRINCIPAIS

### 1. **State Machine** (`state-machine.js`)

**Responsabilidades:**
- Gerenciar estado global da aplicação
- Validar transições entre estados
- Notificar listeners de mudanças
- Atualizar DOM (`data-state` attribute)

**API Pública:**
```javascript
stateMachine.getState()              // Retorna estado atual
stateMachine.transition('ready')     // Muda estado
stateMachine.subscribe(callback)     // Escuta mudanças
stateMachine.canTransition('ar')     // Verifica se pode transitar
```

**Uso:**
```javascript
// Verificar antes de transitar
if (stateMachine.canTransition('ar')) {
    stateMachine.transition('ar');
}

// Escutar mudanças
stateMachine.subscribe((oldState, newState) => {
    console.log(`${oldState} → ${newState}`);
});
```

---

### 2. **AR Manager** (`ar-manager.js`)

**Responsabilidades:**
- Configurar model-viewer com GLB e USDZ
- Validar USDZ com HEAD request (não mostrar botão se inválido)
- Detectar suporte AR (iOS/Android)
- Rastrear eventos AR (`ar-status`)
- Gerenciar UI do botão AR

**Fluxo de Inicialização:**
1. Configura model-viewer com paths GLB/USDZ
2. Envia HEAD request para validar USDZ
3. Detecta device (iOS/Android/Desktop)
4. Define `isARSupported` baseado em device + USDZ válido
5. Espera evento `load` do modelo
6. Mostra botão AR se suportado

**Eventos Rastreados:**
- `load` - Modelo carregou
- `progress` - Atualização de progresso (0-100%)
- `ar-status` - Status da sessão AR
  - `session-started` - AR iniciou
  - `object-placed` - Objeto posicionado
  - `failed` - Erro ao iniciar AR
  - `not-presenting` - AR fechado

**API Pública:**
```javascript
arManager.updateModel(glbPath, usdzPath)  // Trocar modelo
arManager.reset()                         // Reset câmera/estado
```

---

### 3. **Photo Mode** (`photo-mode.js`)

**Responsabilidades:**
- Verificar suporte a getUserMedia
- Solicitar permissão de câmera
- Capturar frame do stream como foto
- Usar foto como background da experiência
- Gerenciar UI de captura

**Fluxo:**
1. Verifica se `navigator.mediaDevices` existe
2. Mostra card "Modo Foto" se suportado
3. Ao ativar: solicita câmera (facing=environment)
4. Stream renderiza em `<video>` fullscreen
5. Botão "Capturar" congela frame em canvas
6. Converte canvas para data URL
7. Define como `background-image` do app
8. Para stream e esconde UI de captura

**Graceful Degradation:**
- Se câmera não suportada: card não aparece
- Se permissão negada: mostra erro amigável
- Feature totalmente opcional

**API Pública:**
```javascript
photoMode.enterPhotoMode()    // Ativa câmera
photoMode.capturePhoto()      // Captura frame
photoMode.exitPhotoMode()     // Para stream
photoMode.clearPhoto()        // Limpa background
```

---

### 4. **App Orchestrator** (`app.js`)

**Responsabilidades:**
- Inicializar todos os componentes
- Configurar produto (nome, paths, descrição)
- Popular informações na UI
- Escutar mudanças de estado
- Gerenciar ciclo de vida (pause/resume)
- Error handling global
- Analytics (se configurado)

**Configuração:**
```javascript
const APP_CONFIG = {
    product: {
        name: 'Produto Premium',
        subtitle: 'Experiência AR',
        description: '...',
        glbPath: './models/product.glb',
        usdzPath: './models/product.usdz'
    },
    analytics: {
        enabled: false,
        debugMode: true
    }
};
```

**API Pública (window.PalcoZero):**
```javascript
PalcoZero.updateProduct(newData)    // Trocar produto
PalcoZero.getState()                // Estado atual
PalcoZero.resetAR()                 // Reset AR
PalcoZero.clearPhoto()              // Limpar foto
PalcoZero.config                    // Acesso à config
```

---

## FLUXO DE DADOS

### Carregamento Inicial

```
1. DOM Ready
   └─► StateMachine: idle

2. App.init()
   └─► StateMachine: idle → loading
   └─► Populate UI
   └─► Init ARManager
   └─► Init PhotoMode

3. ARManager loads model
   └─► HEAD request to validate USDZ
   └─► Check AR support (iOS/Android)
   └─► model-viewer fires 'load' event

4. On 'load' event
   └─► StateMachine: loading → ready
   └─► Show AR button (if supported)
   └─► Fade in content cards
```

### Sessão AR

```
1. User taps AR button
   └─► Track click event
   └─► model-viewer opens AR (Quick Look/Scene Viewer)

2. AR opens
   └─► Fires 'ar-status': session-started
   └─► StateMachine: ready → ar
   └─► Show AR status indicator

3. User places object
   └─► Fires 'ar-status': object-placed
   └─► Update status text

4. User exits AR
   └─► Fires 'ar-status': not-presenting
   └─► StateMachine: ar → ready
   └─► Hide status indicator
```

### Modo Photo

```
1. User taps "Ativar Modo Foto"
   └─► PhotoMode.enterPhotoMode()
   └─► Request camera permission

2. Camera granted
   └─► Start video stream
   └─► StateMachine: ready → photo
   └─► Show camera UI

3. User taps "Capturar"
   └─► Freeze frame to canvas
   └─► Convert to data URL
   └─► Set as background
   └─► Hide camera UI (stay in photo state)

4. User taps "Cancelar"
   └─► Stop stream
   └─► StateMachine: photo → ready
   └─► Clear background (if no photo captured)
```

---

## OTIMIZAÇÕES

### Performance

1. **Lazy Loading**
   - model-viewer carregado do CDN
   - Scripts carregados em ordem
   - CSS crítico inline (se necessário)

2. **Asset Optimization**
   - GLB comprimido (Draco compression)
   - USDZ otimizado (Reality Converter)
   - Texturas power-of-two
   - Poly count reduzido

3. **Rendering**
   - Auto-rotate delay de 3s (não imediato)
   - Pause quando tab hidden
   - Shadow soft para melhor performance

### UX

1. **Loading States**
   - Skeleton imediato
   - Progress bar em tempo real
   - Fade-in gradual de conteúdo

2. **Micro-interactions**
   - 120-180ms timing
   - Cubic-bezier easing
   - Hover states sutis
   - Active states com feedback

3. **Glassmorphism Real**
   - Blur 40px (não excessivo)
   - Opacidade 0.06 (muito sutil)
   - Border semi-transparente
   - Shadow suave

---

## EXTENSIBILIDADE

### Adicionar Novo Estado

```javascript
// 1. Atualizar transitions em state-machine.js
transitions: {
    // ... existentes
    ready: ['ar', 'photo', 'newState'],
    newState: ['ready']
}

// 2. Criar lógica no componente relevante
function onNewState() {
    // Lógica específica
}

// 3. Atualizar CSS para data-state
.app-container[data-state="newState"] .element {
    /* estilos específicos */
}
```

### Adicionar Nova Feature

```javascript
// 1. Criar novo módulo
// new-feature.js
class NewFeature {
    constructor() { /* ... */ }
    init() { /* ... */ }
}
window.NewFeature = NewFeature;

// 2. Inicializar em app.js
function initNewFeature() {
    const feature = new NewFeature();
    console.log('✓ New feature initialized');
}

// 3. Integrar no fluxo se necessário
```

### Trocar Produto Dinamicamente

```javascript
// Via API pública
window.PalcoZero.updateProduct({
    name: 'Novo Produto',
    subtitle: 'Nova experiência',
    description: '...',
    glbPath: './models/new-product.glb',
    usdzPath: './models/new-product.usdz'
});

// Resultado:
// - UI atualizada
// - ARManager recarrega modelos
// - USDZ revalidado
// - Botão AR atualizado
```

---

## DEBUGGING

### Console Logs

```javascript
// State changes
[StateMachine] idle → loading
[StateMachine] loading → ready

// AR events
✓ 3D model loaded
✓ USDZ file validated: ./models/product.usdz
✓ AR supported on this device
AR Status: session-started

// Analytics (se debug mode)
[Analytics] ar_click { product, device, timestamp }
[Analytics] state_change { from, to, timestamp }
```

### Dev Tools

**localStorage debug:**
```javascript
localStorage.setItem('palco-debug', 'true');
// Ativa logs extras
```

**Force state:**
```javascript
stateMachine.transition('ready'); // Manual override
```

**Inspect AR support:**
```javascript
console.log(arManager.isARSupported);
console.log(arManager.isUsdzValid);
```

---

## DEPLOY CHECKLIST

### Produção

- [ ] Minificar CSS/JS
- [ ] Comprimir assets (GLB/USDZ)
- [ ] Configurar cache headers
- [ ] HTTPS ativo
- [ ] CORS configurado
- [ ] Error tracking (Sentry)
- [ ] Analytics configurado
- [ ] DNS atualizado
- [ ] SSL renovado

### Staging/QA

- [ ] Ambiente de teste separado
- [ ] Analytics em debug mode
- [ ] Error logs habilitados
- [ ] Todos os checklists passando

---

## NOTAS TÉCNICAS

### Compatibilidade

- **iOS:** Safari 12+ (ARKit support)
- **Android:** Chrome 79+ (ARCore support)
- **Desktop:** Fallback sem AR, modelo 3D funciona

### Dependências

- **model-viewer 3.4.0** (via CDN)
- **Nenhuma biblioteca extra** (vanilla JS)

### Limitações Conhecidas

1. **AR requer HTTPS** - Não funciona em localhost não-seguro
2. **USDZ iOS-only** - Android usa GLB para AR
3. **Camera permission** - Photo mode requer permissão explícita
4. **File size** - USDZ deve ser < 10MB para Quick Look

---

**Última atualização:** 10 Fevereiro 2026
**Versão:** 1.0 Premium
**Autor:** hackthepack team
