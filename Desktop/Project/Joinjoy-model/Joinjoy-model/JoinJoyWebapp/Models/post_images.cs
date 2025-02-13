using System;
using System.ComponentModel.DataAnnotations;
using System.Reactive;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace JoinJoyWebapp.Models;

[Table("post_images")]
public class post_images : BaseModel
{
    [Key]
    [Required]
    [Column("id")]
    public int Id { get; set; }

    [Required]
    [Column("post_id")]
    public int Post_id { get; set; }

    [Url]
    [Column("image_url")]
    public required string Image_url { get; set; }

    // Relationship
    // Foreign Key connect with Posts
    public Posts Post { get; set; } = null!;
}
