using System;

namespace JoinJoyWebapp.Models;

// model to store JWT for authorization
public class AuthToken
{
    public string AccessToken { get; set; } = string.Empty; // Authenticate with API
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    public long ExpiresIn { get; set; } = 3600; // = 1 hr
    public string RefreshToken { get; set; } = string.Empty; // Use to request a new Access Token
    public string ProviderToken { get; set; } = string.Empty;
    public string ProviderRefreshToken { get; set; } = string.Empty;
    public string TokenType { get; set; } = "Bearer";

    public bool IsExpired => DateTime.UtcNow >= CreatedAt.AddSeconds(ExpiresIn);

    public override string ToString()
    {
        return $"AccessToken: {AccessToken}, ExpiresIn: {ExpiresIn} sec, Expired: {IsExpired}";
    }
}

// model to store user information
// public class UserModel
// {
//     public string Id { get; set; } = string.Empty;
//     public string Email { get; set; } = string.Empty;
//     public string FullName { get; set; } = string.Empty;
//     public string Role { get; set; } = "User";
// }

// model to store "response" after user signin
public class AuthResponse
{
    public AuthToken Token { get; set; } = new AuthToken();
    public Supabase.Gotrue.User User { get; set; } = new();
}