
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("Waiting for server to start...")
    time.sleep(3)

    # 1. Register
    email = f"test_{int(time.time())}@example.com"
    password = "password123"
    print(f"Registering user: {email}")
    res = requests.post(f"{BASE_URL}/api/auth/register", json={"email": email, "password": password})
    assert res.status_code == 200, f"Register failed: {res.text}"
    user_data = res.json()
    print("Register success:", user_data)

    # 2. Login
    print("Logging in...")
    res = requests.post(f"{BASE_URL}/api/auth/login", data={"username": email, "password": password})
    assert res.status_code == 200, f"Login failed: {res.text}"
    token = res.json()["access_token"]
    print("Login success, token received.")
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create Post (Text only for simplicity in script, though API requires file)
    # The API requires a file upload. We'll create a dummy file.
    print("Creating post with image...")
    dummy_file = ("test.jpg", b"dummy image content", "image/jpeg")
    res = requests.post(
        f"{BASE_URL}/api/posts/",
        headers=headers,
        data={"content": "Hello World"},
        files={"file": dummy_file}
    )
    assert res.status_code == 200, f"Create post failed: {res.text}"
    post_data = res.json()
    print("Create post success:", post_data)
    post_id = post_data["id"]

    # 4. List Posts
    print("Listing posts...")
    res = requests.get(f"{BASE_URL}/api/posts/")
    assert res.status_code == 200, f"List posts failed: {res.text}"
    posts = res.json()
    assert len(posts) > 0, "No posts found"
    print(f"List posts success: found {len(posts)} posts")

    # 5. Like Post
    print(f"Liking post {post_id}...")
    res = requests.post(f"{BASE_URL}/api/posts/{post_id}/like", headers=headers)
    assert res.status_code == 200, f"Like post failed: {res.text}"
    print("Like post success")

    # 6. Comment on Post
    print(f"Commenting on post {post_id}...")
    res = requests.post(
        f"{BASE_URL}/api/posts/{post_id}/comments",
        headers=headers,
        json={"comment": "Nice post!"}
    )
    assert res.status_code == 200, f"Comment failed: {res.text}"
    print("Comment success")

    # 7. Delete Post
    print(f"Deleting post {post_id}...")
    res = requests.delete(f"{BASE_URL}/api/posts/{post_id}", headers=headers)
    assert res.status_code == 200, f"Delete post failed: {res.text}"
    print("Delete post success")

    print("\nALL TESTS PASSED!")

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
