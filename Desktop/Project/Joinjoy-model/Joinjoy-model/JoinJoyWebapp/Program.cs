// import library

// build setting
using System.Text;
using System.Text.Json;
using JoinJoyWebapp.Models;
using JoinJoyWebapp.Service;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;


var builder = WebApplication.CreateBuilder(args);
builder.Services.AddControllers();
builder.Services.AddControllersWithViews();


// authentication
builder.Services.AddAuthentication()
    .AddJwtBearer(options => {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            // setting
            ValidateIssuer = false,

            // skip ValidateAudience
            ValidateAudience = true,
            ValidAudience = "https://eifdfdbizfrcjylvyebs.supabase.co", // project-ref from Supabase URL

            // check token exp
            ValidateLifetime = true,
            ClockSkew = TimeSpan.FromMinutes(5),

            // check hook secret key
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes("v1,whsec_uWmp6x9aizCslqncA5QZjPxb3IzPVg0GcT+4Mhtqucd1ccz9Q3JGsQEefydWSFWejHV8rOnFf/OeASXn")),
            
            // token must have exp
            RequireExpirationTime = true,
            
            // token must have secret key
            RequireSignedTokens = true
        };

        options.Events = new JwtBearerEvents
        {
            // event when reive JWT token
            OnMessageReceived = context =>
            {
                // ***create class for store cookie
                // var accessToken = context.Request.Cookies["AccessToken"];
                // var refreshToken = context.Request.Cookies["RefreshToken"];
                // if (!string.IsNullOrEmpty(accessToken) && !string.IsNullOrEmpty(refreshToken)) {
                //     context.Token = accessToken;
                //     await supabase.Auth.SetSession(accessToken, refreshToken);
                // }

                // ***test***
                Console.WriteLine("OnMessageReceived working");

                if (!string.IsNullOrEmpty(context.Token))
                {
                    Console.WriteLine($"JWT Token: {context.Token}");
                }

                return Task.CompletedTask;
            },

            // event when JWT fail
            OnAuthenticationFailed = context =>
            {
                return Task.CompletedTask;
            },

            // event when JWT challenge
            OnChallenge = context =>
            {
                context.HandleResponse();
                context.Response.Redirect("/auth/signin");
                return Task.CompletedTask;
            },

        };
    }
);


// supabase setting
var url = Environment.GetEnvironmentVariable("SUPABASE_URL");
var key = Environment.GetEnvironmentVariable("SUPABASE_KEY");

if (string.IsNullOrEmpty(url) || string.IsNullOrEmpty(key))
{
    throw new InvalidOperationException("Supabase URL or Key is missing.");
}

var options = new Supabase.SupabaseOptions
{
    AutoConnectRealtime = true
};

var supabase = new Supabase.Client(url, key, options);
await supabase.InitializeAsync();

// add supabase client into DI container
builder.Services.AddScoped<Supabase.Client>(_ => supabase);
Console.WriteLine($"Supabase is null : {supabase == null}");

// add services into DI container
builder.Services.AddScoped<AuthService>();
builder.Services.AddHttpContextAccessor();
builder.Services.AddScoped<CookieService>();
// builder.Services.AddScoped<StorageService>();

// build
// ***add DI before build***
var app = builder.Build();

// routing
// ***for testing only***
// GET : /tags
// app.MapGet("/tags", async (Supabase.Client supabaseClient) =>
// {
//     try
//     {
//         var response = await supabaseClient.From<Tags>().Get();

//         Console.WriteLine(response.Content);

//         return Results.Ok("got response tags");
//     }
//     catch (Exception ex)
//     {
//         return Results.Problem($"Error fetching tags: {ex.Message}");
//     }
// });

// app.MapPost("/tags-post", async (Supabase.Client supabaseClient) =>
// {
//     var tag = new Tags
//     {
//         Tag_name = "test1",
//         Category_id = 1
//     };

//     var results = await supabaseClient.From<Tags>().Insert(tag);

//     return Results.Ok($"Inserted tag: {tag.Tag_name}");
// });



// // GET : /categories
// app.MapGet("/categories", async (Supabase.Client supabaseClient) =>
// {
//     try
//     {
//         var response = await supabaseClient.From<Categories>().Get();

//         Console.WriteLine(response.Content);

//         return Results.Ok("got response categories");
//     }
//     catch (Exception ex)
//     {
//         return Results.Problem($"Error fetching tags: {ex.Message}");
//     }
// });

// // GET : /posts
// app.MapGet("/posts", async (Supabase.Client supabaseClient) =>
// {
//     try
//     {
//         var response = await supabaseClient.From<Posts>().Get();

//         Console.WriteLine(response.Content);

//         return Results.Ok("got response posts");
//     }
//     catch (Exception ex)
//     {
//         return Results.Problem($"Error fetching tags: {ex.Message}");
//     }
// });

// GET : /cookies
// app.MapGet("/cookies", (HttpContext httpContext) =>
// {
//     var cookies = httpContext.Request.Cookies;

//     foreach (var cookie in cookies)
//     {
//         Console.WriteLine($"Cookie Name: {cookie.Key}, Cookie Value: {cookie.Value}");
//     }

//     return Results.Ok("Got response cookies");
// });

// app.MapGet("/add-cookie", (HttpContext httpContext) =>
// {
//     httpContext.Response.Cookies.Append("test111111", "value idk", new CookieOptions
//     {
//         Expires = DateTimeOffset.UtcNow.AddHours(1)
//     });

//     return Results.Ok("Cookie added");
// });

// app.MapGet("/login", async (Supabase.Client supabaseClient, AuthService authService) =>
// {
//     var email = "123@gmail.com";
//     var password = "123";

//     try
//     {
//         Console.WriteLine("before signin");
//         var response = await supabaseClient.Auth.SignInWithPassword(email, password);
//         Console.WriteLine("after signin");

//         Console.WriteLine($"response : {response}");

//         if (response != null)
//         {
//             authService.SetAuthToken(response);
//             Console.WriteLine("Login success!");
//         }
//         else
//         {
//             Console.WriteLine("Response is null");
//         }

//         if (response?.User != null)
//         {
//             Console.WriteLine("Claims: " + JsonSerializer.Serialize(response.User));
//         }
//         else
//         {
//             Console.WriteLine("Claims is null or missing.");
//         }
//     }
//     catch (Exception ex)
//     {
//         Console.WriteLine($"Error: {ex.Message}");
//     }

//     return Results.Ok("login success");
// });

// app.MapGet("/get-user", async (Supabase.Client supabaseClient, AuthService authService) =>
// {
//     // Console.WriteLine($"token : {authService.GetAuthToken().AccessToken}");
//     var token = "eyJhbGciOiJIUzI1NiIsImtpZCI6IkZYREh3d0VwaG1tNHhkSXMiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2VpZmRmZGJpemZyY2p5bHZ5ZWJzLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiIwOTIwMGFkYy01NzMyLTQ5NjgtOWY2OC1kOTFhNGU4ZDMxMTUiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzM5NDI3OTg0LCJpYXQiOjE3Mzk0MjQzODQsImVtYWlsIjoiMTIzQGdtYWlsLmNvbSIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoiZW1haWwiLCJwcm92aWRlcnMiOlsiZW1haWwiXX0sInVzZXJfbWV0YWRhdGEiOnsiZW1haWxfdmVyaWZpZWQiOnRydWV9LCJyb2xlIjoiYXV0aGVudGljYXRlZCIsImFhbCI6ImFhbDEiLCJhbXIiOlt7Im1ldGhvZCI6InBhc3N3b3JkIiwidGltZXN0YW1wIjoxNzM5NDI0Mzg0fV0sInNlc3Npb25faWQiOiJmMjczNjU2OS1jNDJlLTQ1ZGUtODMzYS03YmI5MGI4OGE5NmMiLCJpc19hbm9ueW1vdXMiOmZhbHNlfQ.DmEYnFHOIYsOmA1bzVtbZHiFKpHEm3pv5LHTQRaanNE";
//     var user = await supabaseClient.Auth.GetUser(token);
//     Console.WriteLine($"user : {user}");

//     return Results.Ok("get user success");
// });


// app.MapPost("/", async (HttpContext context) =>
// {
//     using var reader = new StreamReader(context.Request.Body);
//     var body = await reader.ReadToEndAsync();

//     Console.WriteLine($"📩 Received Webhook: {body}");

//     return Results.Ok(new { status = "Received" });
// });

app.MapControllers();

app.Run();
