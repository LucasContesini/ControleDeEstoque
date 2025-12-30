let produtos = [];
let produtosFiltrados = [];
let modoEdicao = false;
let especificacoesCount = 0;
let ordenacaoAtual = 'recente';

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
    carregarProdutos();
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
        
        return `
        <div class="produto-card">
            <img src="${imagemFinal}" 
                 alt="${produto.titulo}" 
                 class="produto-imagem"
                 onerror="this.onerror=null; this.src='${IMAGEM_PLACEHOLDER}';">
            <h3 class="produto-titulo">${produto.titulo}</h3>
            <p class="produto-descricao">${produto.descricao || 'Sem descrição'}</p>
            <div class="produto-quantidades">
                <span class="produto-quantidade">Total: ${produto.quantidade}</span>
                <div class="quantidades-ecommerce-display">
                    <span class="quantidade-badge ml">🛒 ML: ${produto.quantidade_mercado_livre || 0}</span>
                    <span class="quantidade-badge shopee">🛍️ Shopee: ${produto.quantidade_shopee || 0}</span>
                </div>
            </div>
            ${renderizarEspecificacoes(produto.especificacoes)}
            <div class="produto-acoes">
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

// Calcular quantidade total automaticamente
function calcularQuantidadeTotal() {
    const quantidade_ml = parseInt(document.getElementById('quantidade_ml').value) || 0;
    const quantidade_shopee = parseInt(document.getElementById('quantidade_shopee').value) || 0;
    const total = quantidade_ml + quantidade_shopee;
    
    document.getElementById('quantidade').value = total;
    document.getElementById('quantidade-total-display').textContent = total;
}

// Configurar campos de quantidade para limpar zero ao focar
function configurarCamposQuantidade() {
    const quantidadeML = document.getElementById('quantidade_ml');
    const quantidadeShopee = document.getElementById('quantidade_shopee');
    
    if (quantidadeML) {
        quantidadeML.addEventListener('focus', function() {
            if (this.value === '0') {
                this.value = '';
            }
        });
        
        quantidadeML.addEventListener('blur', function() {
            if (this.value === '' || this.value === null) {
                this.value = '0';
            }
            calcularQuantidadeTotal();
        });
    }
    
    if (quantidadeShopee) {
        quantidadeShopee.addEventListener('focus', function() {
            if (this.value === '0') {
                this.value = '';
            }
        });
        
        quantidadeShopee.addEventListener('blur', function() {
            if (this.value === '' || this.value === null) {
                this.value = '0';
            }
            calcularQuantidadeTotal();
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
    calcularQuantidadeTotal(); // Inicializar o total
    resetarBotoesFormulario(); // Resetar botões
    configurarCamposQuantidade(); // Configurar campos de quantidade
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
        document.getElementById('quantidade_ml').value = produto.quantidade_mercado_livre || 0;
        document.getElementById('quantidade_shopee').value = produto.quantidade_shopee || 0;
        document.getElementById('imagem').value = produto.imagem || '';
        
        // Calcular quantidade total baseada nas quantidades por e-commerce
        calcularQuantidadeTotal();
        
        // Configurar campos de quantidade para limpar zero ao focar
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
    const quantidade_ml = parseInt(document.getElementById('quantidade_ml').value) || 0;
    const quantidade_shopee = parseInt(document.getElementById('quantidade_shopee').value) || 0;
    const quantidade = quantidade_ml + quantidade_shopee; // Calcular total automaticamente
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
        quantidade_mercado_livre: quantidade_ml,
        quantidade_shopee: quantidade_shopee,
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
}

