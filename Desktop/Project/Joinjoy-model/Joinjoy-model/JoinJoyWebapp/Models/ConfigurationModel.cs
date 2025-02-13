using System;

namespace JoinJoyWebapp.Models;

public class JwtSettings
{
    public string AccessCookie { get; set; } = "AccessToken";
    public string RefreshCookie { get; set; } = "RefreshToken";
}
