// Verificação de versão no app.js - funciona mesmo com HTML antigo
// Versão do script: 2026-01-22-v2 (sempre verifica, mais agressivo)
(function() {
    function mostrarBannerAtualizacao() {
        if (!document.getElementById('version-update-banner')) {
            const banner = document.createElement('div');
            banner.id = 'version-update-banner';
            banner.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; background: #ff9800; color: white; padding: 12px; text-align: center; z-index: 10000; box-shadow: 0 2px 4px rgba(0,0,0,0.2);';
            banner.innerHTML = `
                <span>🔄 Nova versão disponível!</span>
                <button onclick="location.reload(true)" style="margin-left: 15px; padding: 6px 12px; background: white; color: #ff9800; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">Atualizar Agora</button>
                <button onclick="this.parentElement.remove()" style="margin-left: 10px; background: transparent; color: white; border: 1px solid white; padding: 6px 12px; border-radius: 4px; cursor: pointer;">✕</button>
            `;
            if (document.body) {
                document.body.insertBefore(banner, document.body.firstChild);
            } else {
                document.addEventListener('DOMContentLoaded', () => {
                    document.body.insertBefore(banner, document.body.firstChild);
                });
            }
        }
    }
    
    function verificarVersao() {
        fetch('/?check_version=1&_=' + Date.now(), { 
            cache: 'no-store',
            headers: { 
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
        })
            .then(response => {
                if (!response.ok) return null;
                return response.json();
            })
            .then(data => {
                if (data && data.app_version) {
                    const storedVersion = localStorage.getItem('app_version');
                    const storedScriptVersion = localStorage.getItem('script_version');
                    const currentScriptVersion = '2026-01-22-v3';
                    
                    // Se o script mudou, sempre mostrar banner
                    if (storedScriptVersion && storedScriptVersion !== currentScriptVersion) {
                        mostrarBannerAtualizacao();
                        localStorage.setItem('script_version', currentScriptVersion);
                    }
                    
                    // Se a versão do app mudou, mostrar banner
                    if (storedVersion && storedVersion !== data.app_version) {
                        mostrarBannerAtualizacao();
                    }
                    
                    // Sempre atualizar versão salva
                    localStorage.setItem('app_version', data.app_version);
                    if (!storedScriptVersion) {
                        localStorage.setItem('script_version', currentScriptVersion);
                    }
                }
            })
            .catch(() => {});
    }
    
    // Verificar imediatamente ao carregar
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', verificarVersao);
    } else {
        verificarVersao();
    }
    
    // Verificar periodicamente (a cada 30 segundos - mais frequente)
    setInterval(verificarVersao, 30000);
})();

let produtos = [];
let produtosFiltrados = [];
let modoEdicao = false;
let especificacoesCount = 0;
let ordenacaoAtual = 'recente';
let abaAtual = 'produtos';
let vendas = [];
let vendasFiltradas = [];
let observacoesCount = 0;

// Imagem placeholder padrão (caixa de papelão com "Sem Foto")
const IMAGEM_PLACEHOLDER = `data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iI2Y1ZjVmNSIvPgogIDxnIHRyYW5zZm9ybT0idHJhbnNsYXRlKDUwLCA0MCkiPgogICAgPHBhdGggZD0iTSAyMCAzMCBMIDYwIDEwIEwgMTAwIDMwIEwgNjAgNTAgWiIgZmlsbD0iIzhCNDUxMyIgc3Ryb2tlPSIjNjU0MzIxIiBzdHJva2Utd2lkdGg9IjEiLz4KICAgIDxwYXRoIGQ9Ik0gMjAgMzAgTCA2MCA1MCBMIDYwIDkwIEwgMjAgNzAgWiIgZmlsbD0iI0EwNTIyRCIgc3Ryb2tlPSIjNjU0MzIxIiBzdHJva2Utd2lkdGg9IjEiLz4KICAgIDxwYXRoIGQ9Ik0gNjAgNTAgTCAxMDAgMzAgTCAxMDAgNzAgTCA2MCA5MCBaIiBmaWxsPSIjQ0Q4NTNGIiBzdHJva2U9IiM2NTQzMjEiIHN0cm9rZS13aWR0aD0iMSIvPgogICAgPGxpbmUgeDE9IjYwIiB5MT0iMTAiIHgyPSI2MCIgeTI9IjkwIiBzdHJva2U9IiM2NTQzMjEiIHN0cm9rZS13aWR0aD0iMS41Ii8+CiAgICA8cmVjdCB4PSIyNSIgeT0iNDUiIHdpZHRoPSIyMCIgaGVpZ2h0PSIxNSIgZmlsbD0iI2ZmZiIgb3BhY2l0eT0iMC45IiByeD0iMiIvPgogICAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoNzUsIDM1KSI+CiAgICAgIDxlbGxpcHNlIGN4PSIwIiBjeT0iOCIgcng9IjQiIHJ5PSI2IiBmaWxsPSIjMzMzIiBvcGFjaXR5PSIwLjciLz4KICAgICAgPGxpbmUgeDE9Ii0zIiB5MT0iNSIgeDI9IjMiIHkyPSI1IiBzdHJva2U9IiMzMzMiIHN0cm9rZS13aWR0aD0iMSIvPgogICAgPC9nPgogICAgPGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoODUsIDUwKSI+CiAgICAgIDxwYXRoIGQ9Ik0gMCAwIEwgNSA1IEwgLTUgNSBaIiBmaWxsPSIjMzMzIiBvcGFjaXR5PSIwLjciLz4KICAgICAgPHBhdGggZD0iTSAwIDUgTCA1IDEwIEwgLTUgMTAgWiIgZmlsbD0iIzMzMyIgb3BhY2l0eT0iMC43Ii8+CiAgICA8L2c+CiAgPC9nPgogIDx0ZXh0IHg9IjUwJSIgeT0iMTYwIiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9IiM5OTk5OTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtd2VpZ2h0PSI1MDAiPlNlbSBGb3RvPC90ZXh0Pgo8L3N2Zz4=`;

// Função para retornar o placeholder padrão (mantida para compatibilidade)
function gerarPlaceholderProduto(titulo, descricao) {
    return IMAGEM_PLACEHOLDER;
}

// Função para lidar com erro de carregamento de imagem
function tratarErroImagem(img, titulo, descricao) {
    img.onerror = null; // Prevenir loop infinito
    if (titulo) {
        img.src = gerarPlaceholderProduto(titulo, descricao);
    } else {
        img.src = IMAGEM_PLACEHOLDER;
    }
    img.alt = 'Sem foto';
}

// Variáveis para pull-to-refresh
let touchStartY = 0;
let touchEndY = 0;
let isPulling = false;
let pullDistance = 0;
let atualizando = false;
let mouseStartY = 0;
let mouseDown = false;

// Carregar produtos ao iniciar
document.addEventListener('DOMContentLoaded', () => {
    // Configurar data padrão no modal de venda
    document.getElementById('venda-data').value = new Date().toISOString().split('T')[0];
    
    // Carregar conteúdo da aba ativa
    if (abaAtual === 'vendas') {
        carregarVendas();
    } else {
        carregarProdutos();
    }
    
    // Configurar campos de quantidade quando a página carregar
    setTimeout(() => configurarCamposQuantidade(), 100);
    
    const produtosContainer = document.getElementById('produtos-container');
    
    // Função para verificar se está no topo da página
    function estaNoTopo() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        return scrollTop <= 5; // 5px de margem para considerar no topo
    }
    
    // Pull-to-refresh para touch (mobile) - quando puxa para baixo no topo
    let touchStartY = 0;
    let touchEndY = 0;
    let isPulling = false;
    let pullDistance = 0;
    
    window.addEventListener('touchstart', (e) => {
        if (estaNoTopo()) {
            touchStartY = e.touches[0].clientY;
            isPulling = true;
        }
    }, { passive: true });
    
    window.addEventListener('touchmove', (e) => {
        if (isPulling && estaNoTopo()) {
            touchEndY = e.touches[0].clientY;
            pullDistance = touchEndY - touchStartY; // Puxar para baixo = positivo
            
            // Se puxar para baixo (mais de 50px), mostrar indicador visual
            if (pullDistance > 50) {
                produtosContainer.style.transform = `translateY(${Math.min(pullDistance, 100)}px)`;
                produtosContainer.style.transition = 'transform 0.1s';
            }
        } else if (!estaNoTopo()) {
            // Se sair do topo, cancelar o pull
            isPulling = false;
            produtosContainer.style.transform = '';
            produtosContainer.style.transition = '';
            pullDistance = 0;
        }
    }, { passive: true });
    
    window.addEventListener('touchend', () => {
        if (isPulling && estaNoTopo() && pullDistance > 80 && !atualizando) {
            atualizando = true;
            atualizarProdutos(true);
            setTimeout(() => {
                atualizando = false;
            }, 1000);
        }
        
        // Resetar
        produtosContainer.style.transform = '';
        produtosContainer.style.transition = '';
        isPulling = false;
        pullDistance = 0;
    }, { passive: true });
    
    // Pull-to-refresh para mouse (desktop) - quando arrasta para baixo no topo
    let mouseStartY = 0;
    let mouseDown = false;
    
    window.addEventListener('mousedown', (e) => {
        if (estaNoTopo()) {
            mouseStartY = e.clientY;
            mouseDown = true;
        }
    });
    
    window.addEventListener('mousemove', (e) => {
        if (mouseDown && estaNoTopo()) {
            const pullDist = e.clientY - mouseStartY; // Arrastar para baixo = positivo
            if (pullDist > 50) {
                produtosContainer.style.transform = `translateY(${Math.min(pullDist, 100)}px)`;
                produtosContainer.style.transition = 'transform 0.1s';
            }
            pullDistance = pullDist;
        } else if (!estaNoTopo()) {
            // Se sair do topo, cancelar o pull
            mouseDown = false;
            produtosContainer.style.transform = '';
            produtosContainer.style.transition = '';
            pullDistance = 0;
        }
    });
    
    window.addEventListener('mouseup', () => {
        if (mouseDown && estaNoTopo() && pullDistance > 80 && !atualizando) {
            atualizando = true;
            atualizarProdutos(true);
            setTimeout(() => {
                atualizando = false;
            }, 1000);
        }
        
        produtosContainer.style.transform = '';
        produtosContainer.style.transition = '';
        mouseDown = false;
        pullDistance = 0;
    });
});

// Carregar produtos do servidor
async function carregarProdutos() {
    try {
        const response = await fetch('/api/produtos');
        produtos = await response.json();
        produtosFiltrados = [...produtos];
        ordenarProdutos();
    } catch (error) {
        mostrarMensagem('Erro ao carregar produtos: ' + error.message, 'erro');
    }
}

// Atualizar produtos (com loading overlay)
async function atualizarProdutos(silencioso = false) {
    const btnRefresh = document.getElementById('btn-refresh');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    // Desabilitar botão e mostrar loading overlay (sempre, mesmo no pull-to-refresh)
    btnRefresh.disabled = true;
    if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
    }
    
    try {
        const response = await fetch('/api/produtos');
        produtos = await response.json();
        produtosFiltrados = [...produtos];
        
        // Manter ordenação atual
        const ordenacaoAtual = document.getElementById('ordenacao').value;
        ordenarProdutos();
        document.getElementById('ordenacao').value = ordenacaoAtual;
        ordenarProdutos();
        
        if (!silencioso) {
            mostrarMensagem('Produtos atualizados!', 'sucesso');
        }
    } catch (error) {
        if (!silencioso) {
            mostrarMensagem('Erro ao atualizar produtos: ' + error.message, 'erro');
        }
    } finally {
        // Restaurar botão e esconder loading
        btnRefresh.disabled = false;
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    }
}

// Renderizar produtos na tela
function renderizarProdutos(listaProdutos) {
    const container = document.getElementById('produtos-container');
    
    if (listaProdutos.length === 0) {
        container.innerHTML = '<div class="vazio">Nenhum produto cadastrado ainda</div>';
        return;
    }
    
    container.innerHTML = listaProdutos.map(produto => {
        // Detectar se a imagem é URL completa (Supabase) ou caminho local
        let imagemSrc = '';
        if (produto.imagem) {
            if (produto.imagem.startsWith('http://') || produto.imagem.startsWith('https://')) {
                imagemSrc = produto.imagem; // URL completa do Supabase
            } else {
                imagemSrc = `/static/uploads/${produto.imagem}`; // Caminho local
            }
        }
        
        // Usar placeholder padrão se não tiver imagem
        const imagemFinal = produto.imagem ? imagemSrc : IMAGEM_PLACEHOLDER;
        
        const valorCompra = produto.valor_compra ? 
            `💰 Compra: R$ ${parseFloat(produto.valor_compra).toFixed(2).replace('.', ',')}` : 
            '';
        
        return `
        <div class="produto-card">
            <img src="${imagemFinal}" 
                 alt="${produto.titulo}" 
                 class="produto-imagem"
                 onerror="this.onerror=null; this.src='${IMAGEM_PLACEHOLDER}';">
            <h3 class="produto-titulo">${produto.titulo}</h3>
            <p class="produto-descricao">${produto.descricao || 'Sem descrição'}</p>
            <div class="produto-quantidades">
                <span class="produto-quantidade">📦 Estoque: ${produto.quantidade || 0}</span>
                ${valorCompra ? `<div style="margin-top: 8px; color: #28a745; font-weight: 600;">${valorCompra}</div>` : ''}
            </div>
            ${renderizarEspecificacoes(produto.especificacoes)}
            <div class="produto-acoes">
                <button class="btn btn-primary" onclick="abrirModalVenda(${produto.id}, '${produto.titulo.replace(/'/g, "\\'")}', ${produto.valor_compra || 0}, ${produto.quantidade || 0})" style="background: #28a745;">💰 Venda</button>
                <button class="btn btn-success" onclick="editarProduto(${produto.id})">Editar</button>
                <button class="btn btn-danger" onclick="deletarProduto(${produto.id})">Excluir</button>
            </div>
        </div>
    `;
    }).join('');
}

// Renderizar especificações
function renderizarEspecificacoes(especificacoesStr) {
    if (!especificacoesStr) return '';
    
    try {
        const especificacoes = typeof especificacoesStr === 'string' ? 
            JSON.parse(especificacoesStr) : especificacoesStr;
        
        if (Object.keys(especificacoes).length === 0) return '';
        
        return '<div class="produto-especificacoes">' +
            Object.entries(especificacoes).map(([chave, valor]) => 
                `<div><strong>${chave}:</strong> ${valor}</div>`
            ).join('') +
            '</div>';
    } catch (e) {
        return '';
    }
}

// Filtrar produtos
function filtrarProdutos() {
    const busca = document.getElementById('busca').value.toLowerCase();
    if (busca === '') {
        produtosFiltrados = [...produtos];
    } else {
        produtosFiltrados = produtos.filter(produto => 
            produto.titulo.toLowerCase().includes(busca) ||
            (produto.descricao && produto.descricao.toLowerCase().includes(busca))
        );
    }
    ordenarProdutos();
}

// Ordenar produtos
function ordenarProdutos() {
    const ordenacao = document.getElementById('ordenacao').value;
    ordenacaoAtual = ordenacao;
    
    const produtosParaOrdenar = [...produtosFiltrados];
    
    switch(ordenacao) {
        case 'nome':
            produtosParaOrdenar.sort((a, b) => 
                a.titulo.localeCompare(b.titulo, 'pt-BR', { sensitivity: 'base' })
            );
            break;
        case 'nome-desc':
            produtosParaOrdenar.sort((a, b) => 
                b.titulo.localeCompare(a.titulo, 'pt-BR', { sensitivity: 'base' })
            );
            break;
        case 'quantidade':
            produtosParaOrdenar.sort((a, b) => b.quantidade - a.quantidade);
            break;
        case 'quantidade-asc':
            produtosParaOrdenar.sort((a, b) => a.quantidade - b.quantidade);
            break;
        case 'recente':
        default:
            produtosParaOrdenar.sort((a, b) => {
                const dataA = new Date(a.data_atualizacao);
                const dataB = new Date(b.data_atualizacao);
                return dataB - dataA; // Mais recente primeiro
            });
            break;
    }
    
    renderizarProdutos(produtosParaOrdenar);
}

// Configurar campo de quantidade para limpar zero ao focar
function configurarCamposQuantidade() {
    const quantidade = document.getElementById('quantidade');
    
    if (quantidade) {
        quantidade.addEventListener('focus', function() {
            if (this.value === '0') {
                this.value = '';
            }
        });
        
        quantidade.addEventListener('blur', function() {
            if (this.value === '' || this.value === null) {
                this.value = '0';
            }
        });
    }
}

// Função para resetar botões do formulário
function resetarBotoesFormulario() {
    const form = document.getElementById('form-produto');
    if (!form) return;
    
    const btnSalvar = form.querySelector('button[type="submit"]');
    const btnCancelar = form.querySelector('button[type="button"]');
    
    if (btnSalvar) {
        btnSalvar.disabled = false;
        btnSalvar.style.opacity = '1';
        btnSalvar.innerHTML = 'Salvar';
    }
    
    if (btnCancelar) {
        btnCancelar.disabled = false;
        btnCancelar.style.opacity = '1';
    }
}

// Abrir modal para criar produto
function abrirModalCriar() {
    modoEdicao = false;
    document.getElementById('modal-titulo').textContent = 'Novo Produto';
    document.getElementById('form-produto').reset();
    document.getElementById('produto-id').value = '';
    document.getElementById('imagem-preview').innerHTML = '';
    document.getElementById('imagem').value = '';
    especificacoesCount = 0;
    document.getElementById('especificacoes-container').innerHTML = '';
    resetarBotoesFormulario(); // Resetar botões
    configurarCamposQuantidade(); // Configurar campo de quantidade
    document.getElementById('modal-produto').style.display = 'block';
}

// Editar produto
async function editarProduto(id) {
    // Abrir modal imediatamente
    modoEdicao = true;
    document.getElementById('modal-titulo').textContent = 'Editar Produto';
    
    // Limpar formulário e mostrar loading
    document.getElementById('form-produto').reset();
    document.getElementById('produto-id').value = '';
    document.getElementById('imagem-preview').innerHTML = `
        <div class="upload-loading">
            <div class="spinner"></div>
            <p>Carregando produto...</p>
        </div>
    `;
    document.getElementById('especificacoes-container').innerHTML = '';
    
    // Desabilitar campos enquanto carrega
    const form = document.getElementById('form-produto');
    const inputs = form.querySelectorAll('input, textarea, button, select');
    inputs.forEach(input => {
        input.disabled = true;
        if (input.type === 'submit' || input.onclick) {
            input.style.opacity = '0.5';
            input.style.cursor = 'not-allowed';
        }
    });
    
    // Abrir modal
    document.getElementById('modal-produto').style.display = 'block';
    
    try {
        const response = await fetch(`/api/produtos/${id}`);
        const produto = await response.json();
        
        // Preencher campos
        document.getElementById('produto-id').value = produto.id;
        document.getElementById('titulo').value = produto.titulo;
        document.getElementById('descricao').value = produto.descricao || '';
        document.getElementById('quantidade').value = produto.quantidade || 0;
        document.getElementById('valor_compra').value = produto.valor_compra || '';
        document.getElementById('imagem').value = produto.imagem || '';
        
        // Configurar campo de quantidade para limpar zero ao focar
        configurarCamposQuantidade();
        
        // Preview da imagem
        let imagemSrc = IMAGEM_PLACEHOLDER;
        if (produto.imagem) {
            // Detectar se é URL completa (Supabase) ou caminho local
            if (produto.imagem.startsWith('http://') || produto.imagem.startsWith('https://')) {
                imagemSrc = produto.imagem; // URL completa do Supabase
            } else {
                imagemSrc = `/static/uploads/${produto.imagem}`; // Caminho local
            }
        }
        document.getElementById('imagem-preview').innerHTML = 
            `<img src="${imagemSrc}" alt="Preview" onerror="this.onerror=null; this.src='${IMAGEM_PLACEHOLDER}';">`;
        
        // Carregar especificações
        especificacoesCount = 0;
        document.getElementById('especificacoes-container').innerHTML = '';
        if (produto.especificacoes) {
            try {
                const especificacoes = typeof produto.especificacoes === 'string' ? 
                    JSON.parse(produto.especificacoes) : produto.especificacoes;
                Object.entries(especificacoes).forEach(([chave, valor]) => {
                    adicionarEspecificacao(chave, valor);
                });
            } catch (e) {
                console.error('Erro ao carregar especificações:', e);
            }
        }
        
        // Reabilitar campos e resetar botões
        inputs.forEach(input => {
            input.disabled = false;
            if (input.type === 'submit' || input.onclick) {
                input.style.opacity = '1';
                input.style.cursor = '';
            }
        });
        
        // Garantir que o botão de salvar está no estado correto
        const btnSalvar = form.querySelector('button[type="submit"]');
        if (btnSalvar) {
            btnSalvar.disabled = false;
            btnSalvar.style.opacity = '1';
            btnSalvar.innerHTML = 'Salvar';
        }
    } catch (error) {
        // Reabilitar campos mesmo em caso de erro
        inputs.forEach(input => {
            input.disabled = false;
            if (input.type === 'submit' || input.onclick) {
                input.style.opacity = '1';
                input.style.cursor = '';
            }
        });
        
        fecharModal();
        mostrarMensagem('Erro ao carregar produto: ' + error.message, 'erro');
    }
}

// Fechar modal
function fecharModal() {
    resetarBotoesFormulario(); // Resetar botões ao fechar
    document.getElementById('modal-produto').style.display = 'none';
}

// Preview de imagem
async function previewImagem(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const previewContainer = document.getElementById('imagem-preview');
    
    // Mostrar loading
    previewContainer.innerHTML = `
        <div class="upload-loading">
            <div class="spinner"></div>
            <p>Enviando imagem...</p>
        </div>
    `;
    
    // Upload da imagem
    const formData = new FormData();
    formData.append('imagem', file);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        if (response.ok) {
            document.getElementById('imagem').value = data.imagem;
            
            // Preview
            const reader = new FileReader();
            reader.onload = (e) => {
                previewContainer.innerHTML = 
                    `<img src="${e.target.result}" alt="Preview">`;
            };
            reader.readAsDataURL(file);
        } else {
            previewContainer.innerHTML = '';
            mostrarMensagem(data.erro || 'Erro ao fazer upload da imagem', 'erro');
        }
    } catch (error) {
        previewContainer.innerHTML = '';
        mostrarMensagem('Erro ao fazer upload: ' + error.message, 'erro');
    }
}

// Adicionar especificação
function adicionarEspecificacao(chave = '', valor = '') {
    const container = document.getElementById('especificacoes-container');
    const id = especificacoesCount++;
    
    const div = document.createElement('div');
    div.className = 'especificacao-item';
    div.innerHTML = `
        <input type="text" placeholder="Nome da especificação" value="${chave}" 
               class="espec-chave" data-id="${id}">
        <input type="text" placeholder="Valor" value="${valor}" 
               class="espec-valor" data-id="${id}">
        <button type="button" onclick="removerEspecificacao(${id})">Remover</button>
    `;
    container.appendChild(div);
}

// Remover especificação
function removerEspecificacao(id) {
    const items = document.querySelectorAll('.especificacao-item');
    items.forEach(item => {
        const inputs = item.querySelectorAll('input');
        if (inputs[0] && inputs[0].dataset.id == id) {
            item.remove();
        }
    });
}

// Salvar produto
async function salvarProduto(event) {
    event.preventDefault();
    
    const id = document.getElementById('produto-id').value;
    const titulo = document.getElementById('titulo').value;
    const descricao = document.getElementById('descricao').value;
    const quantidade = parseInt(document.getElementById('quantidade').value) || 0;
    const valor_compra = parseFloat(document.getElementById('valor_compra').value) || 0;
    const imagem = document.getElementById('imagem').value;
    
    // Coletar especificações
    const especificacoes = {};
    document.querySelectorAll('.especificacao-item').forEach(item => {
        const chave = item.querySelector('.espec-chave').value.trim();
        const valor = item.querySelector('.espec-valor').value.trim();
        if (chave && valor) {
            especificacoes[chave] = valor;
        }
    });
    
    const produto = {
        titulo,
        descricao,
        quantidade,
        valor_compra: valor_compra,
        imagem,
        especificacoes
    };
    
    // Obter botão de salvar e desabilitar
    const form = event.target;
    const btnSalvar = form.querySelector('button[type="submit"]');
    const btnCancelar = form.querySelector('button[type="button"]');
    
    if (!btnSalvar) {
        console.error('Botão de salvar não encontrado');
        return;
    }
    
    const textoOriginal = btnSalvar.innerHTML;
    
    // Mostrar loading (texto diferente para criar vs atualizar)
    const textoLoading = modoEdicao ? 'Atualizando...' : 'Salvando...';
    btnSalvar.disabled = true;
    btnSalvar.style.opacity = '0.7';
    btnSalvar.innerHTML = `<div class="spinner-small"></div> ${textoLoading}`;
    
    if (btnCancelar) {
        btnCancelar.disabled = true;
        btnCancelar.style.opacity = '0.6';
    }
    
    try {
        const url = modoEdicao ? `/api/produtos/${id}` : '/api/produtos';
        const method = modoEdicao ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(produto)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            mostrarMensagem(data.mensagem || 'Produto salvo com sucesso!', 'sucesso');
            fecharModal();
            await carregarProdutos();
            // Restaurar ordenação após recarregar
            document.getElementById('ordenacao').value = ordenacaoAtual;
            ordenarProdutos();
        } else {
            mostrarMensagem(data.erro || 'Erro ao salvar produto', 'erro');
            // Reabilitar botões em caso de erro
            btnSalvar.disabled = false;
            btnSalvar.style.opacity = '1';
            btnSalvar.innerHTML = textoOriginal;
            if (btnCancelar) {
                btnCancelar.disabled = false;
                btnCancelar.style.opacity = '1';
            }
        }
    } catch (error) {
        mostrarMensagem('Erro ao salvar produto: ' + error.message, 'erro');
        // Reabilitar botões em caso de erro
        btnSalvar.disabled = false;
        btnSalvar.style.opacity = '1';
        btnSalvar.innerHTML = textoOriginal;
        if (btnCancelar) {
            btnCancelar.disabled = false;
            btnCancelar.style.opacity = '1';
        }
    }
}

// Deletar produto
async function deletarProduto(id) {
    if (!confirm('Tem certeza que deseja excluir este produto?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/produtos/${id}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            mostrarMensagem(data.mensagem || 'Produto excluído com sucesso!', 'sucesso');
            await carregarProdutos();
            // Restaurar ordenação após recarregar
            document.getElementById('ordenacao').value = ordenacaoAtual;
            ordenarProdutos();
        } else {
            mostrarMensagem(data.erro || 'Erro ao excluir produto', 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao excluir produto: ' + error.message, 'erro');
    }
}

// Mostrar mensagem
function mostrarMensagem(texto, tipo = 'info') {
    const mensagem = document.getElementById('mensagem');
    mensagem.textContent = texto;
    mensagem.className = `mensagem ${tipo}`;
    mensagem.style.display = 'block';
    
    setTimeout(() => {
        mensagem.style.display = 'none';
    }, 3000);
}

// Fechar modal ao clicar fora
window.onclick = function(event) {
    const modal = document.getElementById('modal-produto');
    if (event.target === modal) {
        fecharModal();
    }
    const modalVenda = document.getElementById('modal-venda');
    if (event.target === modalVenda) {
        fecharModalVenda();
    }
}

// ==================== FUNÇÕES DE ABAS ====================
function mostrarAba(aba) {
    abaAtual = aba;
    
    // Atualizar botões de aba
    document.querySelectorAll('.aba-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(`aba-${aba}`).classList.add('active');
    
    // Mostrar/ocultar conteúdo
    document.querySelectorAll('.aba-content').forEach(content => {
        content.classList.remove('active');
        content.style.display = 'none';
    });
    document.getElementById(`aba-${aba}-content`).classList.add('active');
    document.getElementById(`aba-${aba}-content`).style.display = 'block';
    
    // Mostrar/ocultar botão novo produto
    const btnNovoProduto = document.getElementById('btn-novo-produto');
    if (aba === 'produtos') {
        btnNovoProduto.style.display = 'block';
    } else {
        btnNovoProduto.style.display = 'none';
    }
    
    // Carregar conteúdo da aba
    if (aba === 'vendas') {
        // Limpar busca ao trocar para aba de vendas
        const buscaVendas = document.getElementById('busca-vendas');
        if (buscaVendas) {
            buscaVendas.value = '';
        }
        carregarVendas();
    } else {
        carregarProdutos();
    }
}

function atualizarConteudo() {
    if (abaAtual === 'vendas') {
        carregarVendas();
    } else {
        atualizarProdutos();
    }
}

// ==================== FUNÇÕES DE VENDAS ====================
async function carregarVendas() {
    try {
        const response = await fetch('/api/vendas');
        if (!response.ok) {
            throw new Error('Erro ao carregar vendas');
        }
        vendas = await response.json();
        vendasFiltradas = [...vendas];
        filtrarVendas();
    } catch (error) {
        mostrarMensagem('Erro ao carregar vendas: ' + error.message, 'erro');
    }
}

function filtrarVendas() {
    const busca = document.getElementById('busca-vendas');
    if (!busca) {
        renderizarVendas();
        return;
    }
    
    const termoBusca = busca.value.toLowerCase().trim();
    
    if (termoBusca === '') {
        vendasFiltradas = [...vendas];
    } else {
        vendasFiltradas = vendas.filter(venda => {
            // Buscar por nome do produto
            const produtoMatch = venda.produto_titulo && 
                venda.produto_titulo.toLowerCase().includes(termoBusca);
            
            // Buscar por data (formato brasileiro)
            let dataMatch = false;
            if (venda.data_venda) {
                const partesData = venda.data_venda.split('T')[0].split('-');
                if (partesData.length === 3) {
                    const dataLocal = new Date(parseInt(partesData[0]), parseInt(partesData[1]) - 1, parseInt(partesData[2]));
                    const dataFormatada = dataLocal.toLocaleDateString('pt-BR');
                    dataMatch = dataFormatada.includes(termoBusca);
                }
            }
            
            // Buscar por onde vendeu
            const ondeVendeu = venda.onde_vendeu === 'mercado_livre' ? 'mercado livre' : 'shopee';
            const ondeMatch = ondeVendeu.includes(termoBusca);
            
            // Buscar por observações
            const obsMatch = venda.observacoes && 
                venda.observacoes.toLowerCase().includes(termoBusca);
            
            // Buscar por valores (R$ 100, 100.00, 100,50, etc)
            // Normalizar termo de busca: aceitar tanto ponto quanto vírgula
            const termoNormalizado = termoBusca.replace(',', '.');
            const termoSemSeparador = termoBusca.replace(/[,.]/g, '');
            
            // Função auxiliar para normalizar valores para comparação
            const normalizarValor = (valor) => {
                if (!valor) return '';
                // Converter para string e normalizar para ponto
                const str = valor.toString();
                // Se for número, formatar com 2 casas decimais
                const num = parseFloat(str);
                if (!isNaN(num)) {
                    return num.toFixed(2).replace('.', '');
                }
                return str.replace(/[,.]/g, '');
            };
            
            // Valor de venda: buscar tanto com ponto quanto com vírgula
            let valorVendaMatch = false;
            if (venda.valor_venda) {
                const valorNormalizado = normalizarValor(venda.valor_venda);
                const valorPonto = venda.valor_venda.toFixed(2);
                const valorVirgula = valorPonto.replace('.', ',');
                valorVendaMatch = valorNormalizado.includes(termoSemSeparador) ||
                                 valorPonto.includes(termoNormalizado) || 
                                 valorVirgula.includes(termoBusca) ||
                                 valorPonto.includes(termoBusca.replace(',', '.'));
            }
            
            // Valor de compra: buscar tanto com ponto quanto com vírgula
            let valorCompraMatch = false;
            if (venda.valor_compra) {
                const valorNormalizado = normalizarValor(venda.valor_compra);
                const valorPonto = venda.valor_compra.toFixed(2);
                const valorVirgula = valorPonto.replace('.', ',');
                valorCompraMatch = valorNormalizado.includes(termoSemSeparador) ||
                                  valorPonto.includes(termoNormalizado) || 
                                  valorVirgula.includes(termoBusca) ||
                                  valorPonto.includes(termoBusca.replace(',', '.'));
            }
            
            // Buscar por lucro (valor em reais)
            const lucro = venda.lucro || 0;
            const lucroNormalizado = normalizarValor(lucro);
            const lucroPonto = lucro.toFixed(2);
            const lucroVirgula = lucroPonto.replace('.', ',');
            const lucroMatch = lucroNormalizado.includes(termoSemSeparador) ||
                              lucroPonto.includes(termoNormalizado) || 
                              lucroVirgula.includes(termoBusca) ||
                              lucroPonto.includes(termoBusca.replace(',', '.'));
            
            // Buscar por porcentagem de lucro
            const porcentagemLucro = venda.porcentagem_lucro || 0;
            const porcentagemNormalizada = normalizarValor(porcentagemLucro);
            const porcentagemPonto = porcentagemLucro.toFixed(2);
            const porcentagemVirgula = porcentagemPonto.replace('.', ',');
            const porcentagemMatch = porcentagemNormalizada.includes(termoSemSeparador) ||
                                    porcentagemPonto.includes(termoNormalizado) || 
                                    porcentagemVirgula.includes(termoBusca) ||
                                    porcentagemPonto.includes(termoBusca.replace(',', '.')) ||
                                    (`${porcentagemLucro >= 0 ? '+' : ''}${porcentagemVirgula}%`).toLowerCase().includes(termoBusca);
            
            return produtoMatch || dataMatch || ondeMatch || obsMatch || 
                   valorVendaMatch || valorCompraMatch || lucroMatch || porcentagemMatch;
        });
    }
    
    renderizarVendas();
}

function renderizarVendas() {
    const container = document.getElementById('vendas-container');
    
    if (vendasFiltradas.length === 0) {
        if (vendas.length === 0) {
            container.innerHTML = '<div class="vazio">Nenhuma venda registrada ainda</div>';
        } else {
            container.innerHTML = '<div class="vazio">Nenhuma venda encontrada com o termo buscado</div>';
        }
        return;
    }
    
    // Agrupar vendas por mês/ano e calcular lucro total
    const vendasPorMes = {};
    
    vendasFiltradas.forEach(venda => {
        // Obter mês/ano da venda
        let dataVenda;
        if (venda.data_venda) {
            const partesData = venda.data_venda.split('T')[0].split('-');
            if (partesData.length === 3) {
                dataVenda = new Date(parseInt(partesData[0]), parseInt(partesData[1]) - 1, parseInt(partesData[2]));
            } else {
                dataVenda = new Date(venda.data_venda);
            }
        } else {
            dataVenda = new Date();
        }
        
        const mesAno = dataVenda.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
        const mesAnoKey = `${dataVenda.getFullYear()}-${String(dataVenda.getMonth() + 1).padStart(2, '0')}`;
        
        if (!vendasPorMes[mesAnoKey]) {
            vendasPorMes[mesAnoKey] = {
                label: mesAno.charAt(0).toUpperCase() + mesAno.slice(1), // Capitalizar primeira letra
                vendas: [],
                lucroTotal: 0
            };
        }
        
        vendasPorMes[mesAnoKey].vendas.push(venda);
        vendasPorMes[mesAnoKey].lucroTotal += venda.lucro || 0;
    });
    
    // Ordenar meses (mais recente primeiro)
    const mesesOrdenados = Object.keys(vendasPorMes).sort().reverse();
    
    // Renderizar por grupo
    let html = '';
    
    mesesOrdenados.forEach(mesAnoKey => {
        const grupo = vendasPorMes[mesAnoKey];
        
        // Formatar lucro total
        const lucroTotalFormatado = grupo.lucroTotal.toFixed(2).replace('.', ',');
        const corLucroTotal = grupo.lucroTotal >= 0 ? '#4ade80' : '#f87171';
        const sinalLucro = grupo.lucroTotal >= 0 ? '+' : '';
        
        // Linha separadora do mês/ano com lucro total
        html += `
        <div class="venda-mes-separador">
            <div class="venda-mes-titulo">${grupo.label}</div>
            <div class="venda-mes-lucro" style="color: ${corLucroTotal};">
                Lucro Total: ${sinalLucro}R$ ${lucroTotalFormatado}
            </div>
        </div>`;
        
        // Vendas do mês
        grupo.vendas.forEach(venda => {
            // Converter data corretamente (evitar problema de fuso horário)
            let dataFormatada;
            if (venda.data_venda) {
                // Se a data vem como string "YYYY-MM-DD", tratar como data local
                const partesData = venda.data_venda.split('T')[0].split('-');
                if (partesData.length === 3) {
                    // Criar data local (não UTC) para evitar mudança de dia
                    const dataLocal = new Date(parseInt(partesData[0]), parseInt(partesData[1]) - 1, parseInt(partesData[2]));
                    dataFormatada = dataLocal.toLocaleDateString('pt-BR');
                } else {
                    dataFormatada = new Date(venda.data_venda).toLocaleDateString('pt-BR');
                }
            } else {
                dataFormatada = 'Data não informada';
            }
            
            const ondeVendeu = venda.onde_vendeu === 'mercado_livre' ? '🛒 Mercado Livre' : '🛍️ Shopee';
            const corLucro = venda.lucro >= 0 ? '#28a745' : '#dc3545';
            const corPorcentagem = venda.porcentagem_lucro >= 0 ? '#28a745' : '#dc3545';
            
            html += `
            <div class="venda-card">
                <div class="venda-header">
                    <div class="venda-produto">
                        <h3>${venda.produto_titulo}</h3>
                        <div class="venda-data">📅 ${dataFormatada}</div>
                    </div>
                    <div class="venda-acoes">
                        <button class="btn-editar-venda" onclick="editarVenda(${venda.id})" title="Editar venda">
                            ✏️
                        </button>
                        <button class="btn-deletar-venda" onclick="deletarVenda(${venda.id}, '${venda.produto_titulo.replace(/'/g, "\\'")}')" title="Deletar venda">
                            🗑️
                        </button>
                    </div>
                </div>
                <div class="venda-valores">
                    <div class="venda-valor-item compra">
                        <label>Valor de Compra</label>
                        <div class="valor">R$ ${venda.valor_compra.toFixed(2).replace('.', ',')}</div>
                    </div>
                    <div class="venda-valor-item venda">
                        <label>Valor de Venda</label>
                        <div class="valor">R$ ${venda.valor_venda.toFixed(2).replace('.', ',')}</div>
                    </div>
                    <div class="venda-valor-item lucro">
                        <label>Lucro</label>
                        <div class="valor" style="color: ${corLucro};">R$ ${venda.lucro.toFixed(2).replace('.', ',')}</div>
                    </div>
                    <div class="venda-valor-item porcentagem">
                        <label>% de Lucro</label>
                        <div class="valor" style="color: ${corPorcentagem};">${venda.porcentagem_lucro >= 0 ? '+' : ''}${venda.porcentagem_lucro.toFixed(2)}%</div>
                    </div>
                </div>
                <div class="venda-info">
                    <div class="venda-info-item">
                        ${ondeVendeu}
                    </div>
                </div>
                ${venda.observacoes ? `
                <div class="venda-observacoes">
                    <strong>Observações:</strong>
                    ${venda.observacoes}
                </div>
                ` : ''}
            </div>
            `;
        });
    });
    
    container.innerHTML = html;
}

function abrirModalVenda(produtoId, produtoTitulo, valorCompra, quantidade) {
    // Verificar se há estoque disponível
    if (quantidade <= 0) {
        mostrarMensagem('Produto sem estoque disponível!', 'erro');
        return;
    }
    
    document.getElementById('venda-produto-id').value = produtoId;
    document.getElementById('venda-produto-titulo').value = produtoTitulo;
    document.getElementById('venda-produto-nome').value = produtoTitulo;
    document.getElementById('venda-valor-compra').value = valorCompra || 0;
    document.getElementById('venda-valor-venda').value = '';
    document.getElementById('venda-data').value = new Date().toISOString().split('T')[0];
    document.getElementById('venda-onde').value = '';
    document.getElementById('venda-observacoes-container').innerHTML = '';
    observacoesCount = 0;
    
    // Atualizar resumo
    atualizarResumoVenda();
    
    // Adicionar listener para atualizar resumo
    const valorVendaInput = document.getElementById('venda-valor-venda');
    valorVendaInput.removeEventListener('input', atualizarResumoVenda);
    valorVendaInput.addEventListener('input', atualizarResumoVenda);
    
    document.getElementById('modal-venda').style.display = 'block';
}

function fecharModalVenda() {
    // Reabilitar botão caso esteja desabilitado
    const btnSalvar = document.querySelector('#form-venda button[type="submit"]');
    if (btnSalvar) {
        btnSalvar.disabled = false;
        btnSalvar.textContent = 'Registrar Venda';
    }
    
    // Limpar campos
    document.getElementById('venda-id').value = '';
    document.getElementById('modal-venda-titulo').textContent = 'Registrar Venda';
    document.getElementById('venda-produto-nome').readOnly = false;
    document.getElementById('venda-produto-nome').style.background = '#f5f5f5';
    
    document.getElementById('modal-venda').style.display = 'none';
    document.getElementById('form-venda').reset();
    document.getElementById('venda-observacoes-container').innerHTML = '';
    observacoesCount = 0;
}

async function editarVenda(vendaId) {
    try {
        const response = await fetch(`/api/vendas/${vendaId}`);
        if (!response.ok) {
            throw new Error('Erro ao carregar venda');
        }
        const venda = await response.json();
        
        // Preencher modal com dados da venda
        document.getElementById('venda-id').value = venda.id;
        document.getElementById('venda-produto-id').value = venda.produto_id || '';
        document.getElementById('venda-produto-titulo').value = venda.produto_titulo;
        document.getElementById('venda-produto-nome').value = venda.produto_titulo;
        document.getElementById('venda-produto-nome').readOnly = true;
        document.getElementById('venda-produto-nome').style.background = '#f5f5f5';
        document.getElementById('venda-valor-compra').value = venda.valor_compra || 0;
        document.getElementById('venda-valor-venda').value = venda.valor_venda || '';
        
        // Formatar data para o input date (YYYY-MM-DD)
        const dataVenda = venda.data_venda ? venda.data_venda.split('T')[0] : new Date().toISOString().split('T')[0];
        document.getElementById('venda-data').value = dataVenda;
        document.getElementById('venda-onde').value = venda.onde_vendeu || '';
        
        // Preencher observações
        document.getElementById('venda-observacoes-container').innerHTML = '';
        observacoesCount = 0;
        if (venda.observacoes) {
            const obsArray = venda.observacoes.split(' | ');
            obsArray.forEach(obs => {
                if (obs.trim()) {
                    const id = observacoesCount++;
                    const div = document.createElement('div');
                    div.className = 'especificacao-item';
                    div.innerHTML = `
                        <input type="text" placeholder="Observação" class="obs-chave" data-id="${id}" value="${obs.trim().replace(/"/g, '&quot;')}">
                        <button type="button" onclick="removerObservacao(${id})">Remover</button>
                    `;
                    document.getElementById('venda-observacoes-container').appendChild(div);
                }
            });
        }
        
        // Atualizar título do modal e botão
        document.getElementById('modal-venda-titulo').textContent = 'Editar Venda';
        const btnSalvar = document.querySelector('#form-venda button[type="submit"]');
        if (btnSalvar) {
            btnSalvar.textContent = 'Salvar Alterações';
        }
        
        // Atualizar resumo
        atualizarResumoVenda();
        
        // Adicionar listener para atualizar resumo
        const valorVendaInput = document.getElementById('venda-valor-venda');
        valorVendaInput.removeEventListener('input', atualizarResumoVenda);
        valorVendaInput.addEventListener('input', atualizarResumoVenda);
        
        document.getElementById('modal-venda').style.display = 'block';
    } catch (error) {
        console.error('Erro ao carregar venda:', error);
        mostrarMensagem('Erro ao carregar venda: ' + error.message, 'erro');
    }
}

async function deletarVenda(vendaId, produtoTitulo) {
    if (!confirm(`Tem certeza que deseja deletar a venda de "${produtoTitulo}"?\n\nEsta ação irá restaurar 1 unidade no estoque do produto (se ainda existir).`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/vendas/${vendaId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.erro || 'Erro ao deletar venda');
        }
        
        mostrarMensagem('Venda deletada com sucesso!', 'sucesso');
        
        // Recarregar vendas e produtos
        await carregarVendas();
        await carregarProdutos();
    } catch (error) {
        console.error('Erro ao deletar venda:', error);
        mostrarMensagem('Erro ao deletar venda: ' + error.message, 'erro');
    }
}

function atualizarResumoVenda() {
    const valorCompra = parseFloat(document.getElementById('venda-valor-compra').value) || 0;
    const valorVenda = parseFloat(document.getElementById('venda-valor-venda').value) || 0;
    const resumo = document.getElementById('venda-resumo');
    
    if (valorVenda > 0) {
        const lucro = valorVenda - valorCompra;
        const porcentagem = valorCompra > 0 ? (lucro / valorCompra * 100) : 0;
        
        document.getElementById('venda-resumo-compra').textContent = 
            `R$ ${valorCompra.toFixed(2).replace('.', ',')}`;
        document.getElementById('venda-resumo-venda').textContent = 
            `R$ ${valorVenda.toFixed(2).replace('.', ',')}`;
        document.getElementById('venda-resumo-lucro').textContent = 
            `R$ ${lucro.toFixed(2).replace('.', ',')}`;
        document.getElementById('venda-resumo-porcentagem').textContent = 
            `${porcentagem >= 0 ? '+' : ''}${porcentagem.toFixed(2)}%`;
        
        resumo.style.display = 'block';
    } else {
        resumo.style.display = 'none';
    }
}

function adicionarObservacao() {
    const container = document.getElementById('venda-observacoes-container');
    const id = observacoesCount++;
    
    const div = document.createElement('div');
    div.className = 'especificacao-item';
    div.innerHTML = `
        <input type="text" placeholder="Observação" class="obs-chave" data-id="${id}">
        <button type="button" onclick="removerObservacao(${id})">Remover</button>
    `;
    container.appendChild(div);
}

function removerObservacao(id) {
    const items = document.querySelectorAll('#venda-observacoes-container .especificacao-item');
    items.forEach(item => {
        const input = item.querySelector('.obs-chave');
        if (input && input.dataset.id == id) {
            item.remove();
        }
    });
}

async function salvarVenda(event) {
    event.preventDefault();
    
    const vendaId = document.getElementById('venda-id').value;
    const produtoId = parseInt(document.getElementById('venda-produto-id').value);
    const valorVenda = parseFloat(document.getElementById('venda-valor-venda').value);
    const dataVenda = document.getElementById('venda-data').value;
    const ondeVendeu = document.getElementById('venda-onde').value;
    const isEdicao = vendaId && vendaId !== '';
    
    // Validações básicas
    if (!isEdicao && (!produtoId || produtoId <= 0)) {
        mostrarMensagem('Produto inválido', 'erro');
        return;
    }
    
    if (!valorVenda || valorVenda <= 0) {
        mostrarMensagem('Valor de venda deve ser maior que zero', 'erro');
        return;
    }
    
    if (!dataVenda) {
        mostrarMensagem('Data da venda é obrigatória', 'erro');
        return;
    }
    
    if (!ondeVendeu) {
        mostrarMensagem('Selecione onde vendeu', 'erro');
        return;
    }
    
    // Coletar observações
    const observacoesArray = [];
    document.querySelectorAll('#venda-observacoes-container .obs-chave').forEach(input => {
        const obs = input.value.trim();
        if (obs) {
            observacoesArray.push(obs);
        }
    });
    const observacoes = observacoesArray.join(' | ');
    
    const venda = {
        produto_id: produtoId,
        valor_venda: valorVenda,
        data_venda: dataVenda,
        onde_vendeu: ondeVendeu,
        observacoes: observacoes
    };
    
    const btnSalvar = event.target.querySelector('button[type="submit"]');
    if (!btnSalvar) {
        console.error('Botão de salvar não encontrado');
        return;
    }
    
    const textoOriginal = btnSalvar.innerHTML;
    btnSalvar.disabled = true;
    btnSalvar.innerHTML = isEdicao ? 'Salvando...' : 'Registrando...';
    
    // Timeout de segurança (30 segundos)
    const timeoutId = setTimeout(() => {
        btnSalvar.disabled = false;
        btnSalvar.innerHTML = textoOriginal;
        mostrarMensagem('Tempo de espera excedido. Tente novamente.', 'erro');
    }, 30000);
    
    // Garantir que o botão seja sempre reabilitado, mesmo em caso de erro
    try {
        const url = isEdicao ? `/api/vendas/${vendaId}` : '/api/vendas';
        const method = isEdicao ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(venda)
        });
        
        clearTimeout(timeoutId);
        
        let data;
        try {
            data = await response.json();
        } catch (jsonError) {
            // Se não conseguir parsear JSON, tentar ler como texto
            const textResponse = await response.text();
            console.error('Erro ao parsear JSON:', textResponse);
            btnSalvar.disabled = false;
            btnSalvar.innerHTML = textoOriginal;
            mostrarMensagem('Resposta inválida do servidor. Tente novamente.', 'erro');
            return;
        }
        
        if (response.ok) {
            mostrarMensagem(isEdicao ? 'Venda atualizada com sucesso!' : 'Venda registrada com sucesso!', 'sucesso');
            fecharModalVenda();
            // Atualizar produtos e vendas
            try {
                await carregarProdutos();
                await carregarVendas();
            } catch (updateError) {
                console.error('Erro ao atualizar após venda:', updateError);
            }
        } else {
            mostrarMensagem(data.erro || (isEdicao ? 'Erro ao atualizar venda' : 'Erro ao registrar venda'), 'erro');
            btnSalvar.disabled = false;
            btnSalvar.innerHTML = textoOriginal;
        }
    } catch (error) {
        clearTimeout(timeoutId);
        console.error('Erro ao salvar venda:', error);
        mostrarMensagem('Erro ao salvar venda: ' + (error.message || 'Erro desconhecido'), 'erro');
        // Sempre reabilitar o botão em caso de erro
        btnSalvar.disabled = false;
        btnSalvar.innerHTML = textoOriginal;
    }
}

