<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Instagram Clone</title>

  <!-- ✅ Define Backend IP here -->
  <meta name="backend-url" content="http://192.168.1.100:5000">

  <style>
    body { font-family: yellow, sans-serif; margin: 30px; }
    h2, h4 { colour: #444; }
    form { margin-bottom: 20px; }
    input, button { padding: 8px; margin: 5px; }
    .post { border: 1px solid #ccc; padding: 10px; margin-bottom: 20px; }
    img { max-width: 300px; display: block; margin-top: 10px; }
  </style>
</head>
<body>

  <h1>📸 Instagram Clone</h1>

  <!-- Register Form -->
  <h3>Register</h3>
  <form id="registerForm">
    <input type="text" id="regUsername" placeholder="Username" required>
    <input type="password" id="regPassword" placeholder="Password" required>
    <button type="submit">Register</button>
  </form>

  <!-- Login Form -->
  <h3>Login</h3>
  <form id="loginForm">
    <input type="text" id="loginUsername" placeholder="Username" required>
    <input type="password" id="loginPassword" placeholder="Password" required>
    <button type="submit">Login</button>
  </form>

  <p id="status"></p>

  <!-- Upload Section -->
  <div id="uploadSection" style="display:none;">
    <h3>Upload Post</h3>
    <form id="uploadForm">
      <input type="text" id="caption" placeholder="Caption" required><br>
      <input type="file" id="image" accept="image/*" required><br>
      <button type="submit">Upload</button>
    </form>
  </div>

  <!-- Feed -->
  <h3>Feed</h3>
  <div id="feed"></div>

  <!-- ✅ JavaScript Section -->
  <script>
    const BACKEND_URL = document.querySelector('meta[name="backend-url"]').content;
    let userId = null;

    // Register
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = document.getElementById('regUsername').value;
      const password = document.getElementById('regPassword').value;

      const res = await fetch(`${BACKEND_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const data = await res.json();
      alert(data.message || data.error);
    });

    // Login
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const username = document.getElementById('loginUsername').value;
      const password = document.getElementById('loginPassword').value;

      const res = await fetch(`${BACKEND_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const data = await res.json();
      if (data.user_id) {
        userId = data.user_id;
        document.getElementById('status').innerText = `✅ Logged in as ${username}`;
        document.getElementById('uploadSection').style.display = 'block';
      } else {
        alert(data.error);
      }
    });

    // Upload Post
    document.getElementById('uploadForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const caption = document.getElementById('caption').value;
      const image = document.getElementById('image').files[0];

      const formData = new FormData();
      formData.append('user_id', userId);
      formData.append('caption', caption);
      formData.append('image', image);

      const res = await fetch(`${BACKEND_URL}/upload`, {
        method: 'POST',
        body: formData
      });

      const data = await res.json();
      alert(data.message || data.error);
      loadFeed(); // Refresh the feed
    });

    // Load Feed
    async function loadFeed() {
      const res = await fetch(`${BACKEND_URL}/feed`);
      const posts = await res.json();

      const feed = document.getElementById('feed');
      feed.innerHTML = '';

      posts.forEach(post => {
        const div = document.createElement('div');
        div.className = 'post';
        div.innerHTML = `
          <strong>@${post.username}</strong>
          <p>${post.caption}</p>
          <img src="${BACKEND_URL + post.image_url}" alt="Post image">
          <small>${new Date(post.upload_time).toLocaleString()}</small>
        `;
        feed.appendChild(div);
      });
    }

    // Load feed on page load
    loadFeed();
  </script>
</body>
</html>


