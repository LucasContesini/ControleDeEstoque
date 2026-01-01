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
    
    // Configurar drag and drop
    configurarDragAndDrop();
    
    // Garantir que o campo de busca está configurado
    const buscaInput = document.getElementById('busca');
    if (buscaInput) {
        buscaInput.addEventListener('input', filtrarProdutos);
        buscaInput.addEventListener('keyup', filtrarProdutos);
    }
    
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
        paginaAtual = 1; // Resetar para primeira página
        atualizarCategorias(); // Atualizar lista de categorias
        ordenarProdutos();
        atualizarEstatisticas(); // Atualizar estatísticas após carregar produtos
        
        // Esconder loading inicial após carregar
        const loadingInicial = document.getElementById('loading-inicial');
        if (loadingInicial) {
            loadingInicial.style.display = 'none';
        }
    } catch (error) {
        mostrarMensagem('Erro ao carregar produtos: ' + error.message, 'erro');
        // Esconder loading mesmo em caso de erro
        const loadingInicial = document.getElementById('loading-inicial');
        if (loadingInicial) {
            loadingInicial.style.display = 'none';
        }
    }
}

// Atualizar lista de categorias
function atualizarCategorias() {
    const categorias = new Set();
    produtos.forEach(produto => {
        if (produto.categoria && produto.categoria.trim()) {
            categorias.add(produto.categoria.trim());
        }
    });
    
    const filtroCategoria = document.getElementById('filtro-categoria');
    const datalistCategorias = document.getElementById('categorias-lista');
    
    if (filtroCategoria) {
        // Limpar opções existentes (exceto "Todas")
        filtroCategoria.innerHTML = '<option value="">📂 Todas as categorias</option>';
        categorias.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat;
            option.textContent = cat;
            filtroCategoria.appendChild(option);
        });
    }
    
    if (datalistCategorias) {
        datalistCategorias.innerHTML = '';
        categorias.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat;
            datalistCategorias.appendChild(option);
        });
    }
}

// Atualizar estatísticas
function atualizarEstatisticas() {
    const totalProdutos = produtos.length;
    const totalEstoque = produtos.reduce((sum, p) => sum + (p.quantidade || 0), 0);
    const estoqueBaixo = produtos.filter(p => (p.quantidade || 0) === 0).length;
    
    document.getElementById('total-produtos').textContent = totalProdutos;
    document.getElementById('total-estoque').textContent = totalEstoque;
    document.getElementById('estoque-baixo').textContent = estoqueBaixo;
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
        
        atualizarEstatisticas(); // Atualizar estatísticas após atualizar produtos
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
        const busca = document.getElementById('busca').value.toLowerCase();
        const mensagem = busca ? 'Nenhum produto encontrado' : 'Nenhum produto cadastrado ainda';
        container.innerHTML = `<div class="vazio">${mensagem}</div>`;
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
        
        // Verificar se estoque está baixo (quantidade = 0)
        const estoqueBaixo = (produto.quantidade || 0) === 0;
        const faixaEstoqueBaixo = estoqueBaixo ? '<div class="faixa-estoque-baixo">ESTOQUE BAIXO</div>' : '';
        const categoriaBadge = produto.categoria ? `<span class="produto-categoria">${produto.categoria}</span>` : '';
        
        return `
        <div class="produto-card ${estoqueBaixo ? 'estoque-baixo' : ''}">
            ${faixaEstoqueBaixo}
            <img src="${imagemFinal}" 
                 alt="${produto.titulo}" 
                 class="produto-imagem"
                 ${produto.imagem ? 'loading="lazy"' : ''}
                 onerror="this.onerror=null; this.src='${IMAGEM_PLACEHOLDER}';">
            <h3 class="produto-titulo">${produto.titulo}</h3>
            ${categoriaBadge}
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
// Debounce para busca (aguarda 300ms após parar de digitar)
let buscaTimeout = null;

function filtrarProdutos() {
    // Limpar timeout anterior
    if (buscaTimeout) {
        clearTimeout(buscaTimeout);
    }
    
    // Aguardar 300ms antes de filtrar
    buscaTimeout = setTimeout(() => {
        const buscaInput = document.getElementById('busca');
        if (!buscaInput) {
            console.error('Campo de busca não encontrado');
            return;
        }
        
        const busca = buscaInput.value.toLowerCase().trim();
        const categoriaFiltro = document.getElementById('filtro-categoria')?.value || '';
        
        // Verificar se produtos está carregado
        if (!produtos || produtos.length === 0) {
            console.warn('Produtos ainda não foram carregados');
            return;
        }
        
        // Aplicar filtros
        produtosFiltrados = produtos.filter(produto => {
            // Filtro por categoria
            if (categoriaFiltro && produto.categoria !== categoriaFiltro) {
                return false;
            }
            
            // Se não há busca, retornar true (já passou pelo filtro de categoria)
            if (busca === '') {
                return true;
            }
            
            // Buscar no título
            if (produto.titulo && produto.titulo.toLowerCase().includes(busca)) return true;
            
            // Buscar na descrição
            if (produto.descricao && produto.descricao.toLowerCase().includes(busca)) return true;
            
            // Buscar na categoria
            if (produto.categoria && produto.categoria.toLowerCase().includes(busca)) return true;
            
            // Buscar nas especificações
            if (produto.especificacoes) {
                try {
                    const especificacoes = typeof produto.especificacoes === 'string' 
                        ? JSON.parse(produto.especificacoes) 
                        : produto.especificacoes;
                    
                    if (typeof especificacoes === 'object' && especificacoes !== null) {
                        for (const [chave, valor] of Object.entries(especificacoes)) {
                            if (chave.toLowerCase().includes(busca) || 
                                String(valor).toLowerCase().includes(busca)) {
                                return true;
                            }
                        }
                    }
                } catch (e) {
                    console.warn('Erro ao processar especificações:', e);
                }
            }
            
            return false;
        });
        ordenarProdutos();
    }, 300);
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

// Carregar imagens lazy quando visíveis
function carregarImagensLazy() {
    const imagens = document.querySelectorAll('.lazy-load[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy-load');
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            });
        });
        
        imagens.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback para navegadores antigos
        imagens.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy-load');
            img.removeAttribute('data-src');
        });
    }
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
        document.getElementById('categoria').value = produto.categoria || '';
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

// Comprimir imagem usando Canvas
function comprimirImagem(file, maxWidth = 1920, maxHeight = 1920, quality = 0.8) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                let width = img.width;
                let height = img.height;
                
                // Redimensionar se necessário
                if (width > maxWidth || height > maxHeight) {
                    const ratio = Math.min(maxWidth / width, maxHeight / height);
                    width = width * ratio;
                    height = height * ratio;
                }
                
                canvas.width = width;
                canvas.height = height;
                
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);
                
                // Converter para blob
                canvas.toBlob((blob) => {
                    if (blob) {
                        resolve(blob);
                    } else {
                        reject(new Error('Erro ao comprimir imagem'));
                    }
                }, 'image/jpeg', quality);
            };
            img.onerror = reject;
            img.src = e.target.result;
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Preview de imagem com compressão e barra de progresso
async function previewImagem(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Validar tamanho (máximo 10MB antes de compressão)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
        mostrarToast('Imagem muito grande! Máximo 10MB.', 'erro');
        event.target.value = '';
        return;
    }
    
    const previewContainer = document.getElementById('imagem-preview');
    
    // Mostrar barra de progresso
    previewContainer.innerHTML = `
        <div class="upload-progress-container">
            <div class="upload-progress-bar">
                <div class="upload-progress-fill" id="upload-progress-fill" style="width: 0%"></div>
            </div>
            <p class="upload-progress-text" id="upload-progress-text">Comprimindo imagem...</p>
        </div>
    `;
    
    const progressFill = document.getElementById('upload-progress-fill');
    const progressText = document.getElementById('upload-progress-text');
    
    try {
        // Atualizar progresso
        progressFill.style.width = '30%';
        progressText.textContent = 'Comprimindo imagem...';
        
        // Comprimir imagem
        const compressedFile = await comprimirImagem(file);
        
        progressFill.style.width = '60%';
        progressText.textContent = 'Enviando para servidor...';
        
        // Upload da imagem comprimida
        const formData = new FormData();
        formData.append('imagem', compressedFile, file.name);
        
        // Simular progresso do upload (já que fetch não tem progresso nativo)
        const progressInterval = setInterval(() => {
            const currentWidth = parseInt(progressFill.style.width);
            if (currentWidth < 90) {
                progressFill.style.width = (currentWidth + 5) + '%';
            }
        }, 100);
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        clearInterval(progressInterval);
        progressFill.style.width = '100%';
        progressText.textContent = 'Concluído!';
        
        const data = await response.json();
        if (response.ok) {
            document.getElementById('imagem').value = data.imagem;
            
            // Preview da imagem comprimida
            const reader = new FileReader();
            reader.onload = (e) => {
                previewContainer.innerHTML = 
                    `<img src="${e.target.result}" alt="Preview" class="imagem-preview-img">`;
            };
            reader.readAsDataURL(compressedFile);
            
            // Mostrar tamanho reduzido se houver redução significativa
            const tamanhoOriginal = (file.size / 1024).toFixed(1);
            const tamanhoComprimido = (compressedFile.size / 1024).toFixed(1);
            if (compressedFile.size < file.size * 0.9) {
                mostrarToast(`Imagem comprimida: ${tamanhoOriginal}KB → ${tamanhoComprimido}KB`, 'sucesso');
            }
        } else {
            previewContainer.innerHTML = '';
            mostrarToast(data.erro || 'Erro ao fazer upload da imagem', 'erro');
        }
    } catch (error) {
        previewContainer.innerHTML = '';
        mostrarToast('Erro ao processar imagem: ' + error.message, 'erro');
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
    const titulo = document.getElementById('titulo').value.trim();
    const descricao = document.getElementById('descricao').value.trim();
    const categoria = document.getElementById('categoria').value.trim();
    
    // Validar quantidades (não permitir negativas)
    let quantidade_ml = parseInt(document.getElementById('quantidade_ml').value) || 0;
    let quantidade_shopee = parseInt(document.getElementById('quantidade_shopee').value) || 0;
    
    // Garantir que não sejam negativas
    if (quantidade_ml < 0) {
        quantidade_ml = 0;
        document.getElementById('quantidade_ml').value = 0;
        mostrarToast('Quantidade do Mercado Livre não pode ser negativa', 'aviso');
    }
    if (quantidade_shopee < 0) {
        quantidade_shopee = 0;
        document.getElementById('quantidade_shopee').value = 0;
        mostrarToast('Quantidade da Shopee não pode ser negativa', 'aviso');
    }
    
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
        categoria,
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
            const mensagem = modoEdicao ? `"${titulo}" atualizado com sucesso!` : `"${titulo}" criado com sucesso!`;
            mostrarToast(mensagem, 'sucesso');
            fecharModal();
            await carregarProdutos();
            // Restaurar ordenação após recarregar
            document.getElementById('ordenacao').value = ordenacaoAtual;
            ordenarProdutos();
        } else {
            mostrarToast(data.erro || 'Erro ao salvar produto', 'erro');
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
        mostrarToast('Erro ao salvar produto: ' + error.message, 'erro');
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

// Duplicar produto
// Deletar produto com confirmação melhorada
async function deletarProduto(id) {
    // Buscar nome do produto para mostrar na confirmação
    const produto = produtos.find(p => p.id === id);
    const nomeProduto = produto ? produto.titulo : 'este produto';
    
    // Modal de confirmação customizado
    if (!confirm(`⚠️ Tem certeza que deseja excluir "${nomeProduto}"?\n\nEsta ação não pode ser desfeita.`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/produtos/${id}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            mostrarToast(`"${nomeProduto}" excluído com sucesso!`, 'sucesso');
            await carregarProdutos();
            // Restaurar ordenação após recarregar
            document.getElementById('ordenacao').value = ordenacaoAtual;
            ordenarProdutos();
        } else {
            mostrarToast(data.erro || 'Erro ao excluir produto', 'erro');
        }
    } catch (error) {
        mostrarToast('Erro ao excluir produto: ' + error.message, 'erro');
    }
}

// Sistema de Toast Notifications
function mostrarToast(mensagem, tipo = 'info') {
    // Remover toasts anteriores
    const toastsExistentes = document.querySelectorAll('.toast');
    toastsExistentes.forEach(toast => toast.remove());
    
    // Criar novo toast
    const toast = document.createElement('div');
    toast.className = `toast toast-${tipo}`;
    
    // Ícone baseado no tipo
    const icones = {
        'sucesso': '✅',
        'erro': '❌',
        'aviso': '⚠️',
        'info': 'ℹ️'
    };
    
    toast.innerHTML = `
        <span class="toast-icon">${icones[tipo] || icones.info}</span>
        <span class="toast-mensagem">${mensagem}</span>
        <button class="toast-fechar" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    document.body.appendChild(toast);
    
    // Animação de entrada
    setTimeout(() => toast.classList.add('toast-show'), 10);
    
    // Remover automaticamente após 4 segundos
    setTimeout(() => {
        toast.classList.remove('toast-show');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Manter função antiga para compatibilidade (deprecated)
function mostrarMensagem(texto, tipo = 'info') {
    mostrarToast(texto, tipo);
}

// Fechar modal ao clicar fora
window.onclick = function(event) {
    const modal = document.getElementById('modal-produto');
    if (event.target === modal) {
        fecharModal();
    }
}

// Atalhos de teclado
document.addEventListener('keydown', function(event) {
    // Ctrl+N ou Cmd+N para novo produto
    if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
        event.preventDefault();
        const modal = document.getElementById('modal-produto');
        if (modal.style.display !== 'block') {
            abrirModalCriar();
        }
    }
    
    // Esc para fechar modal
    if (event.key === 'Escape') {
        const modal = document.getElementById('modal-produto');
        if (modal.style.display === 'block') {
            fecharModal();
        }
    }
    
    // Enter para salvar (se estiver no modal e não estiver em textarea)
    if (event.key === 'Enter' && !event.shiftKey) {
        const modal = document.getElementById('modal-produto');
        const activeElement = document.activeElement;
        if (modal.style.display === 'block' && 
            activeElement.tagName !== 'TEXTAREA' && 
            activeElement.type !== 'submit') {
            const form = document.getElementById('form-produto');
            if (form && !activeElement.closest('.especificacao-item')) {
                event.preventDefault();
                form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
            }
        }
    }
});

// Exportar produtos para CSV
async function exportarCSV() {
    try {
        const response = await fetch('/api/produtos/exportar-csv');
        
        if (!response.ok) {
            const error = await response.json();
            mostrarToast(error.erro || 'Erro ao exportar CSV', 'erro');
            return;
        }
        
        // Obter o blob do CSV
        const blob = await response.blob();
        
        // Criar link de download
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `controle-estoque-${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        mostrarToast('CSV exportado com sucesso!', 'sucesso');
    } catch (error) {
        mostrarToast('Erro ao exportar CSV: ' + error.message, 'erro');
    }
}

// Importar produtos de CSV
async function importarCSV(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    if (!file.name.endsWith('.csv')) {
        mostrarToast('Por favor, selecione um arquivo CSV', 'erro');
        event.target.value = '';
        return;
    }
    
    const formData = new FormData();
    formData.append('arquivo', file);
    
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
        loadingOverlay.querySelector('p').textContent = 'Importando produtos...';
    }
    
    try {
        const response = await fetch('/api/produtos/importar-csv', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            mostrarToast(`✅ ${data.mensagem || 'Produtos importados com sucesso!'}`, 'sucesso');
            await carregarProdutos();
            // Restaurar ordenação após recarregar
            document.getElementById('ordenacao').value = ordenacaoAtual;
            ordenarProdutos();
        } else {
            mostrarToast(data.erro || 'Erro ao importar CSV', 'erro');
        }
    } catch (error) {
        mostrarToast('Erro ao importar CSV: ' + error.message, 'erro');
    } finally {
        // Limpar input
        event.target.value = '';
        if (loadingOverlay) {
            loadingOverlay.style.display = 'none';
        }
    }
}

