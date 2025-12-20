from modules.login_register import register, login

# Test register
print("Testing register...")
# Simulate input for register
import builtins
original_input = builtins.input
builtins.input = lambda prompt: "testuser" if "username" in prompt else "testpass"
register()

builtins.input = lambda prompt: "testuser2" if "username" in prompt else "testpass2"
register()

# Test login success
print("\nTesting login success...")
builtins.input = lambda prompt: "testuser" if "username" in prompt else "testpass"
login()

# Test login fail
print("\nTesting login fail...")
builtins.input = lambda prompt: "wronguser" if "username" in prompt else "wrongpass"
login()

# Restore input
builtins.input = original_input