using System;
using System.ComponentModel.DataAnnotations;
using System.Reactive;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace JoinJoyWebapp.Models;

[Table("post_tags")]
public class post_tags : BaseModel
{
    [Key]
    [Required]
    [Column("id")]
    public int Id { get; set; }

    [Required]
    [Column("post_id")]
    public int Post_id { get; set; }

    [Required]
    [Column("tag_id")]
    public int Tag_id { get; set; }
}
