using System;
using System.ComponentModel.DataAnnotations;
using System.Reactive;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace JoinJoyWebapp.Models;

[Table("tags")]
public class Tags : BaseModel
{
    [PrimaryKey("id", false)]
    public int Id { get; set; }

    [Column("tag_name")]
    public string Tag_name { get; set; } = string.Empty;

    [Column("category_id")]
    public int Category_id { get; set; }

    // Relationship
    // Foreign Key connect with Category
    // public Categories Category { get; set; } = null!;
}

public class Tag : BaseModel
{
    public string Tag_name { get; set; } = string.Empty;

    public long Category_id { get; set; }

}

public class TagsDto
    {
        public int Id {get; set;}
        public string Tag_name { get; set; } = string.Empty;
        public long Category_id { get; set; }
    }
