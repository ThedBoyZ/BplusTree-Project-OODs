using System;
using System.ComponentModel.DataAnnotations;
using System.Reactive;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace JoinJoyWebapp.Models;

[Table("user_joints")]
public class user_joints : BaseModel
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
}
