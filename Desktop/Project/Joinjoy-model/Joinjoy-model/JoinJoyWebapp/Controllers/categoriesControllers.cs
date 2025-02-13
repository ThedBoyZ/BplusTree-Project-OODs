using Supabase;
using System.Diagnostics;
using JoinJoyWebapp.Models;
using Microsoft.AspNetCore.Mvc;
using JoinJoyWebapp.Service;

public class categoriesControllers : Controller
{
    private readonly Client _supabaseClient;

    public categoriesControllers (Client supabaseClient)

    {
        _supabaseClient = supabaseClient;
    }

    
    [HttpGet("/categories")]
     public async Task<IActionResult> GetCategories()
    {
        try{
            var response = await _supabaseClient.From<Categories>().Get();

              var CategoriesDtos = response.Models.Select(cat => new CategoriesDto
                {
                    Id = cat.Id,
                    Category_name = cat.Category_name,
                }).ToList();
                Console.WriteLine(response.Content);
                return View(CategoriesDtos);
        }
        catch (Exception ex)
        {
            
            return Problem($"Error fetching tags: {ex.Message}");
        }
    }


}