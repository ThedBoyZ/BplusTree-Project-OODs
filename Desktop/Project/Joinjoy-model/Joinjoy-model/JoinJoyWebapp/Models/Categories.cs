using System;
using System.ComponentModel.DataAnnotations;
using Supabase.Postgrest.Attributes;
using Supabase.Postgrest.Models;

namespace JoinJoyWebapp.Models;

[Table("categories")]
public class Categories : BaseModel
{
    [Key]
    [Column("id")]
    public int Id { get; set; }

    [Column("category_name")]
    public string Category_name { get; set; } = string.Empty;

    // Relationship
    // One Category many Tags
    public List<Tags> Tags { get; set; } = new List<Tags>();
}

public class CategoriesDto
    {
        public int Id {get; set;}
        public string Category_name { get; set; } = string.Empty;
    }
