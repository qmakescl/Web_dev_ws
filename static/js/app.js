// --- API Helper ---
const api = {
    async request(url, options = {}) {
        const token = localStorage.getItem('token');
        if (token) {
            options.headers = {
                ...options.headers,
                'Authorization': `Bearer ${token}`
            };
        }
        const response = await fetch(url, options);
        if (response.status === 401) {
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return response;
    },

    async get(url) {
        return this.request(url);
    },

    async post(url, data, isFormData = false) {
        const options = {
            method: 'POST',
            body: isFormData ? data : JSON.stringify(data)
        };
        if (!isFormData) {
            options.headers = { 'Content-Type': 'application/json' };
        }
        return this.request(url, options);
    }
};

// --- Auth Functions ---
async function handleRegister(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const res = await api.post('/api/auth/register', { email, password });
    if (res.ok) {
        alert('회원가입 성공! 로그인해주세요.');
        window.location.href = '/login';
    } else {
        const data = await res.json();
        alert(data.detail || '회원가입 실패');
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const res = await api.post('/api/auth/login', formData, true);
    if (res.ok) {
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        window.location.href = '/';
    } else {
        alert('로그인 실패: 이메일 또는 비밀번호를 확인하세요.');
    }
}

function handleLogout() {
    localStorage.removeItem('token');
    window.location.href = '/login';
}

// --- Post Functions ---
async function loadPosts(tag = null) {
    const url = tag ? `/api/tags/${tag}` : '/api/posts';
    const res = await api.get(url);
    if (!res.ok) return;

    const posts = await res.json();
    const feed = document.getElementById('feed');
    if (!feed) return;

    if (posts.length === 0) {
        feed.innerHTML = '<div style="text-align:center; padding:20px;">게시물이 없습니다.</div>';
        return;
    }

    feed.innerHTML = posts.map(post => `
        <article class="post-card">
            <header class="post-header">User ${post.user_id}</header>
            <img src="${post.img_path}" class="post-image" alt="Post">
            <div class="post-actions">
                <button onclick="toggleLike(${post.id})">❤️</button>
                <button onclick="location.href='/posts/${post.id}'">💬</button>
            </div>
            <div class="post-content">
                <span class="username">User ${post.user_id}</span>
                ${linkifyTags(post.content || '')}
            </div>
        </article>
    `).join('');
}

function linkifyTags(text) {
    return text.replace(/#(\w+)/g, '<span class="hashtag" onclick="loadPosts(\'$1\')" style="color:#00376b; cursor:pointer;">#$1</span>');
}

async function handleSearch(e) {
    e.preventDefault();
    const query = document.getElementById('search-input').value.trim();
    if (query) {
        loadPosts(query);
    } else {
        loadPosts();
    }
}

async function handleCreatePost(e) {
    e.preventDefault();
    const formData = new FormData(e.target);

    const res = await api.post('/api/posts/', formData, true);
    if (res.ok) {
        window.location.reload();
    } else {
        alert('업로드 실패');
    }
}

async function toggleLike(postId) {
    const res = await api.post(`/api/posts/${postId}/like`, {});
    if (res.ok) {
        const data = await res.json();
        console.log(data.message);
        // UI 업데이트 로직 (생략 가능하나 넣으면 좋음)
    }
}

// --- Utils ---
function toggleModal(id, show) {
    document.getElementById(id).style.display = show ? 'block' : 'none';
}
