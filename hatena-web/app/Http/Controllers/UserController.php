<?php

namespace App\Http\Controllers;

use App\User;
use Goutte\Client;
use Illuminate\Support\Facades\DB;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class UserController extends Controller
{

    public function show(string $id)
    {
        $user = User::where('id', $id)->first();
        return $user ?? abort(404);
    }

    public function followers(string $id)
    {
        $users = User::select('id', 'icon', 'url', 'follower_total', 'bio')
            ->join('follows', 'users.id', '=', 'follows.follow_by')
            ->where('follows.follow_to', '=', $id)
            ->orderBy('follower_total', 'DESC')->paginate(20);

        return $users ?? abort(404);
    }

    public function followings(string $id)
    {
        $users = User::select('id', 'icon', 'url', 'follower_total', 'bio')
            ->join('follows', 'users.id', '=', 'follows.follow_to')
            ->where('follows.follow_by', '=', $id)
            ->orderBy('follower_total', 'DESC')->paginate(20);

        return $users ?? abort(404);
    }

    public function archive(string $id)
    {
        $user = User::where('id', $id)->firstOrFail();

        $client = new Client();
       $client->setHeader('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36');
        // $crawler = $client->request('GET', $user->url);
        $client->request('GET', 'https://delete-all.hatenablog.com/archive');
        // $currentUrl = $client->getHistory()->current()->getUri();
        // $client->request('GET', $currentUrl . 'archive/');
        // $client->request('GET', 'https://delete-all.hatenablog.com/archive');
        Log::info($currentUrl);

        $links = [];
        $crawler->filter('section.archive-entry.autopagerize_page_element')->each(function($element) use (&$links) {
            $links[] =  [
                'entry-title' => $element->filter('h1.entry-title')->text(),
                'href' => $element->filter('a')->attr('href'),
                'content' => $element->filter('p.entry-description')->text()
            ];
        });

        Log::info($links[0]['href']);

        return $links ?? abort(404);
    }
}
