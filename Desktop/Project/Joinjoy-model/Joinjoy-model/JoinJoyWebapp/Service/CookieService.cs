using System;

namespace JoinJoyWebapp.Service;

public class CookieService
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public CookieService(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public void SetCookie(string key, string value)
    {
        var options = new CookieOptions
        {
            Expires = DateTime.UtcNow.AddHours(1),
            // HttpOnly = true,
            // Secure = true,
            // SameSite = SameSiteMode.Strict
        };

        _httpContextAccessor.HttpContext?.Response.Cookies.Append(key, value, options);
        Console.WriteLine("set cookie success");
    }

    public string? GetCookie(string key)
    {
        string? value = null;
        _httpContextAccessor.HttpContext?.Request.Cookies.TryGetValue(key, out value);
        return value;
    }

    public void DeleteCookie(string key)
    {
        _httpContextAccessor.HttpContext?.Response.Cookies.Delete(key);
    }
}