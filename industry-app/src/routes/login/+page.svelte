<script>
    let isLogin = true;
    let email = '';
    let password = '';

    const toggleForm = () => {
        isLogin = !isLogin;
    };

    const handleSubmit = () => {
        // Add logic for form submission here
        console.log(isLogin ? 'Logging in...' : 'Signing up...', { email, password });
    };
</script>

<style>
.background-image {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('/background.jpg') no-repeat center center;
    background-size: cover;
    z-index: -1;
}

.login-container {
    background: rgba(0, 0, 0, 0.5);
    padding: 2rem;
    border-radius: 30px;
    max-width: 600px;
    text-align: center;
}

.login-container h1 {
    color: #fff;
    font-size: 4rem;
}

.toggle-buttons {
    display: flex;
    margin-bottom: 1.5rem;
    width: 100%;
}

.toggle-buttons button {
    flex: 1;
    padding: 0.5rem;
    border: none;
    background: #6ec3c4;
    color: #fff;
    cursor: pointer;
    transition: background 0.3s ease;
    border-radius: 5px;
}

.toggle-buttons button.active {
    background: #fff;
    color: #6ec3c4;
}

.form-group {
    width: 100%;
}

.form-group input {
    width: 99%;
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
    margin-top: 0.5rem;
    border-radius: 5px;
    border: none;
    font-size: 1rem;
}

.submit-button {
    background: #6ec3c4;
    color: #fff;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 5px;
    cursor: pointer;
    transition: background 0.3s ease;
    width: 100%;
    margin-top: 1.5rem;
}

.submit-button:hover {
    background: #fff;
    color: #6ec3c4;
}
</style>


<div class="background-image"></div>

<div class="login-container">
    <h1>TRAC Application</h1>
    <div class="toggle-buttons">
        <button class={isLogin ? 'active' : ''} on:click={toggleForm}>
            Login
        </button>
        <button class={!isLogin ? 'active' : ''} on:click={toggleForm}>
            Sign Up
        </button>
    </div>

    <div class="form-group">
        <input type="email" id="email" bind:value={email} placeholder="Email Address" required />
    </div>
    <div class="form-group">
        <input type="password" id="password" bind:value={password} placeholder="Password" required />
    </div>
    <button class="submit-button" on:click={handleSubmit}>
        {isLogin ? 'LOG IN' : 'SIGN UP'}
    </button>
</div>
