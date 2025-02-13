using System;
using System.ComponentModel.DataAnnotations;
using System.Reactive;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace JoinJoyWebapp.Models;

[Table("profiles")]
public class Profiles : BaseModel
{
    [Required]
    [Column("id")]
    public int Id { get; set; }

    [Required]
    [Column("user_id")]
    public required string User_id { get; set; }

    [Required]
    [Column("username")]
    public required string Username { get; set; }

    [Column("bio")]
    public required string Bio { get; set; }

    [Url]
    [Column("avatar_url")]
    public required string Avatar_url { get; set; }

    // Relationship
    // One profile connect with one user
    public Users User { get; set; } = null!;
}
