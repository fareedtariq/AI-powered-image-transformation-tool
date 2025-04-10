<?php

use Illuminate\Support\Facades\Route;
use Inertia\Inertia;

Route::get('/', function () {
    // return Inertia::render('welcome');
    return redirect('/dashboard');
})->name('home');

Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');

    Route::post('/process-image', [ImageController::class, 'processImage'])->middleware('auth');

});

require __DIR__.'/settings.php';
require __DIR__.'/auth.php';
