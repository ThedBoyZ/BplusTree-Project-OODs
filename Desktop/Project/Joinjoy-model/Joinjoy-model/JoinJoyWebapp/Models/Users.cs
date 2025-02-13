using System;
using System.ComponentModel.DataAnnotations;

namespace JoinJoyWebapp.Models;

public class Users
{
    [Required]
    public required string Id { get; set; }  // User ID from Supabase

    [EmailAddress]
    [Required]
    public required string Email { get; set; } // User email from Supabase

    // Relationship
    // One user one profile
    public Profiles Profile { get; set; } = null!;
    // One user many post
    public required List<user_posts> user_posts { get; set; }
    // One use many like
    public required List<user_likes> user_likes { get; set; }
    // One user many join
    public required List<user_joints> user_joints { get; set; }
}
