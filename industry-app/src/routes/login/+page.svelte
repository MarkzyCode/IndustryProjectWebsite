<script>
    // Global variables
    let isLogin = true;
    let email = '';
    let password = '';

    // Function to toggle the form
    const toggleForm = () => {
        isLogin = !isLogin;
    };

    // Function to handle form submission
    const handleSubmit = () => {
        // Add logic for form submission here
        console.log(isLogin ? 'Logging in...' : 'Signing up...', { email, password });
    };
</script>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login or Create an Account | TRAC</title>
    <link rel="stylesheet" href="./src/styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
</head>

<div class="background-image"></div>

<div class="login-flex">
    <div class="login-container">
        <h1>TRAC Application</h1>
        <div class="toggle-buttons">
            <button class={isLogin ? 'active' : ''} on:click={toggleForm}>
                Sign Up
            </button>
            <button class={!isLogin ? 'active' : ''} on:click={toggleForm}>
                Login
            </button>
        </div>
    
        <div class="form-group">
            <input class="login-input" type="email" id="email" bind:value={email} placeholder="Email Address" required />
        </div>
        <div class="form-group">
            <input class="login-input" type="password" id="password" bind:value={password} placeholder="Password" required />
        </div>
        <div class="login-buttons">
            <button class="submit-button" on:click={handleSubmit}>{isLogin ? 'LOGIN' : 'SIGN UP'}</button>
        </div>
        <br>
        <a href="/" class="back-button">Back</a>
    </div>
</div>