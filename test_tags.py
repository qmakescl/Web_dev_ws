import requests
import os

# Configuration
BASE_URL = "http://localhost:8000/api"
EMAIL = "test_tag@example.com"
PASSWORD = "password123"

def run_test():
    session = requests.Session()

    # 1. Register
    print("1. Registering new user...")
    res = session.post(f"{BASE_URL}/auth/register", json={"email": EMAIL, "password": PASSWORD})
    if res.status_code == 200:
        print("   Success")
    elif res.status_code == 400 and "already exists" in res.text:
        print("   User already exists, proceeding...")
    else:
        print(f"   Failed: {res.text}")
        return

    # 2. Login
    print("2. Logging in...")
    res = session.post(f"{BASE_URL}/auth/login", data={"username": EMAIL, "password": PASSWORD})
    if res.status_code == 200:
        token = res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("   Success")
    else:
        print(f"   Failed: {res.text}")
        return

    # 3. Create Post with Tag
    print("3. Creating post with tag #test_tag...")
    with open("test_image.jpg", "wb") as f:
        f.write(os.urandom(1024))  # Dummy image
    
    files = {"file": ("test_image.jpg", open("test_image.jpg", "rb"), "image/jpeg")}
    data = {"content": "This is a post with #test_tag and #awesome"}
    
    res = requests.post(f"{BASE_URL}/posts/", headers=headers, files=files, data=data)
    os.remove("test_image.jpg")
    
    if res.status_code == 200:
        post_id = res.json()["id"]
        print(f"   Success: Post ID {post_id}")
    else:
        print(f"   Failed: {res.text}")
        return

    # 4. Search by Tag
    print("4. Searching for tag 'test_tag'...")
    res = requests.get(f"{BASE_URL}/tags/test_tag")
    if res.status_code == 200:
        posts = res.json()
        found = any(p["id"] == post_id for p in posts)
        if found:
            print(f"   Success: Found {len(posts)} posts. Confirmed created post is in results.")
        else:
            print("   Failed: Post not found in tag search results.")
    else:
        print(f"   Failed: {res.text}")

    # Clean up (Delete post)
    print("5. Deleting post...")
    res = requests.delete(f"{BASE_URL}/posts/{post_id}", headers=headers)
    if res.status_code == 200:
        print("   Success")

if __name__ == "__main__":
    run_test()
