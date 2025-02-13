using System;
using System.ComponentModel.DataAnnotations;
using System.Reactive;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace JoinJoyWebapp.Models;

public enum PostState
{
    join,
    full,
    close
}

[Table("posts")]
public class Posts : BaseModel
{
    [Key]
    [Column("id")]
    public int Id { get; set; }

    [Column("user_id")]
    public string User_id { get; set; } = string.Empty;

    [Column("title")]
    public string Title { get; set; } = string.Empty;

    [Column("content")]
    public string Content { get; set; } = string.Empty;

    [Column("post_state")]
    public PostState Post_state { get; set; }

    [Column("closing_date")]
    public DateTime Closing_date { get; set; }

    [Column("activity_start_date")]
    public DateTime Activity_start_date { get; set; }

    [Url]
    [Column("location_url")]
    public string Location_url { get; set; } = string.Empty;

    [Column("province")]
    public string Province { get; set; } = string.Empty;

    [Column("district")]
    public string District { get; set; } = string.Empty;

    [Column("sub_district")]
    public string Sub_district { get; set; } = string.Empty;

    [Column("number_of_people")]
    public int Number_of_people { get; set; }

    [Column("number_of_views")]
    public int Number_of_views { get; set; }

    [Column("created_at")]
    public DateTime Created_at { get; set; }

    // // Relationship
    // // One Post many image
    // public List<post_images> post_images { get; set; }
    // // One Post many tag
    // public List<post_tags> post_tags { get; set; }
    // // One Post many like
    // public List<user_likes> user_likes { get; set; }
    // // One Post many join
    // public List<user_joints> user_joints { get; set; }

    // // Foreign Key connect with User
    // public Users User { get; set; } = null!;
}
