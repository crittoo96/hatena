<?php

use Illuminate\Http\Request;
use \App\User;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/
//Route::get('/user', fn() => Auth::user())->name('user');
Route::get('/users/{id}', 'UserController@show')->name('user.show');
Route::get('/users/{id}/followers', 'UserController@followers');
Route::get('/users/{id}/followings', 'UserController@followings');
Route::get('/users/{id}/archive', 'UserController@archive');
