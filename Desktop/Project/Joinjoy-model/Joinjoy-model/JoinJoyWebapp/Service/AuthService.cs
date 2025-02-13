using System;
using JoinJoyWebapp.Models;
using Microsoft.AspNetCore.Components.Authorization;
using Microsoft.VisualBasic;
using Supabase.Gotrue;

namespace JoinJoyWebapp.Service;

// handle token -> connect with AuthModel
public class AuthService
    {
        private readonly ILogger<AuthService> _logger;
        private AuthToken _authToken = new();
        private AuthResponse _authResponse = new();
        private CookieService _cookieService;

        public AuthService(ILogger<AuthService> logger, CookieService cookieService)
        {
            _logger = logger;
            _cookieService = cookieService;
        }

        public void SetAuthToken(Supabase.Gotrue.Session response)
        {
            _authToken.AccessToken = response?.AccessToken ?? string.Empty;
            _authToken.CreatedAt = response?.CreatedAt ?? DateTime.UtcNow;
            _authToken.ExpiresIn = response?.ExpiresIn ?? 0;
            _authToken.RefreshToken = response?.RefreshToken ?? string.Empty;
            _authToken.ProviderToken = response?.ProviderToken ?? string.Empty;
            _authToken.ProviderRefreshToken = response?.ProviderRefreshToken ?? string.Empty;
            _authToken.TokenType = response?.TokenType ?? string.Empty;

            _authResponse.Token = _authToken;
            _authResponse.User = response?.User ?? new();

            _cookieService.SetCookie("AccessToken", _authToken.AccessToken);
            _cookieService.SetCookie("RefreshToken",_authToken.RefreshToken);

            _logger.LogInformation($"🔑 AccessToken Updated: {_authToken.AccessToken}");
        }

        public bool IsAuthenticated()
        {
            return !string.IsNullOrEmpty(_authResponse.Token.AccessToken) && !_authResponse.Token.IsExpired;
        }

        public AuthToken GetAuthToken()
        {
            return _authResponse.Token;
        }

        public Supabase.Gotrue.User GetUser()
        {
            return _authResponse.User;
        }

        public void ClearAuth()
        {
            _authResponse = new AuthResponse();
            _logger.LogInformation("🚪 User logged out.");
        }
    }
