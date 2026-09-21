// Configuração do Supabase
const SUPABASE_URL = 'https://htxxeruauqgsqmrkvkbm.supabase.co';
const SUPABASE_KEY = 'sb_publishable_ygeKzjfX35YhkROX9_N_eg_bMEewsPW';

const _supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

let votoSelecionado = '';

// Elementos da tela
const likeBtn = document.getElementById('like-btn');
const dislikeBtn = document.getElementById('dislike-btn');
const commentContainer = document.getElementById('feedback-comment-container');
const commentInput = document.getElementById('feedback-comment');
const sendBtn = document.getElementById('send-feedback-btn');
const thanksMsg = document.getElementById('feedback-thanks');

// Clique no botão de Like
if (likeBtn) {
  likeBtn.addEventListener('click', () => {
    votoSelecionado = 'like';
    commentContainer.classList.remove('hidden');
  });
}

// Clique no botão de Dislike
if (dislikeBtn) {
  dislikeBtn.addEventListener('click', () => {
    votoSelecionado = 'dislike';
    commentContainer.classList.remove('hidden');
  });
}

// Clique no botão de Enviar
if (sendBtn) {
  sendBtn.addEventListener('click', async () => {
    const comentarioTexto = commentInput.value;

    // Grava no banco do Supabase
    const { error } = await _supabase
      .from('feedbacks')
      .insert([
        { tipo: votoSelecionado, comentario: comentarioTexto }
      ]);

    if (!error) {
      commentContainer.classList.add('hidden');
      likeBtn.parentElement.classList.add('hidden'); // esconde os botões de like/dislike
      thanksMsg.classList.remove('hidden'); // exibe a mensagem de obrigado
    } else {
      console.error('Erro ao enviar feedback:', error);
      alert('Ops! Houve um erro ao salvar seu feedback.');
    }
  });
}