SUPPORTED_PROVIDERS = {
        "google": {
            "server_metadata_url": "https://accounts.google.com/.well-known/openid-configuration",
            "client_kwargs": {"scope": "openid email profile"},
        },
        "github": {
            "authorize_url": "https://github.com/login/oauth/authorize",
            "access_token_url": "https://github.com/login/oauth/access_token",
            "api_base_url": "https://api.github.com/",
            "client_kwargs": {"scope": "user:email"},
        },
        "facebook": {
            "authorize_url": "https://www.facebook.com/v12.0/dialog/oauth",
            "access_token_url": "https://graph.facebook.com/v12.0/oauth/access_token",
            "api_base_url": "https://graph.facebook.com/",
            "client_kwargs": {"scope": "public_profile email user_gender"},
        }
    }