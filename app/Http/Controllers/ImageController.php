<?php

use App\Http\Controllers\Controller;
use App\Models\Image;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Storage;

class ImageController extends Controller
{
    public function processImage(Request $request)
    {
        $request->validate([
            'image' => 'required|image|mimes:jpeg,png,jpg|max:2048',
            'style_1' => 'required|integer',
            'style_2' => 'nullable|integer',
            'alpha' => 'nullable|numeric|min:0|max:1',
        ]);

        $image = $request->file('image');
        $imagePath = $image->store('uploads', 'public'); // Store image in Laravel

        // Send the image to Python API
        $response = Http::attach(
            'image', file_get_contents(storage_path("app/public/{$imagePath}")), $image->getClientOriginalName()
        )->post('http://127.0.0.1:8000/apply-style/', [
            'style_1' => $request->style_1,
            'style_2' => $request->style_2,
            'alpha' => $request->alpha
        ]);

        if ($response->failed()) {
            return response()->json(['error' => 'Image processing failed'], 500);
        }

        // Save processed image path
        $processedImagePath = 'processed/' . time() . '.png';
        Storage::disk('public')->put($processedImagePath, $response->body());

        // Save record in DB
        $imageRecord = Image::create([
            'user_id' => auth()->id(),
            'image_path' => $processedImagePath,
            'style_1' => $request->style_1,
            'style_2' => $request->style_2,
            'alpha' => $request->alpha,
        ]);

        return response()->json(['image_path' => asset("storage/{$processedImagePath}")]);
    }
}
