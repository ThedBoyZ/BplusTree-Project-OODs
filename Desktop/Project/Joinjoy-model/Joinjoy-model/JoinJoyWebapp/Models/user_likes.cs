using System;
using System.ComponentModel.DataAnnotations;
using System.Reactive;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace JoinJoyWebapp.Models;

[Table("user_likes")]
public class user_likes : BaseModel
{
    [Key]
    [Required]
    [Column("id")]
    public int Id { get; set; }

    [Required]
    [Column("user_id")]
    public required string User_id { get; set; }

    [Required]
    [Column("post_id")]
    public int Post_id { get; set; }

    // Relationship
    // Foreign Key to User
    public required Users User { get; set; }
    // Foreign Key to Post
    public required Posts Post { get; set; }
}
