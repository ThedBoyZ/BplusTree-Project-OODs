using Supabase;
using System.Diagnostics;
using JoinJoyWebapp.Models;
using Microsoft.AspNetCore.Mvc;
using JoinJoyWebapp.Service;

public class tagsControllers : Controller
{
    private readonly Client _supabaseClient;

    public tagsControllers (Client supabaseClient)

    {
        _supabaseClient = supabaseClient;
    }

    
    [HttpGet("/tags")]
     public async Task<IActionResult> GetTags()
    {
        try{
            var response = await _supabaseClient.From<Tags>().Get();

              var tagsDtos = response.Models.Select(tag => new TagsDto
                {
                    Id = tag.Id,
                    Tag_name = tag.Tag_name,
                    Category_id = tag.Category_id
                }).ToList();
                
                Console.WriteLine(response.Content);
                return View(tagsDtos);
        }
        catch (Exception ex)
        {
            
            return Problem($"Error fetching tags: {ex.Message}");
        }
    }


}