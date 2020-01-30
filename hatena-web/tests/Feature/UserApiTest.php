<?php

namespace Tests\Feature;

use App\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Foundation\Testing\WithFaker;
use Tests\TestCase;

class UserApiTest extends TestCase
{
    /** @test */
    public function should_正しい構造のJSONを返却する()
    {
        $user = User::first();

        $response = $this->json('GET', route('user.show', [
            'id' => $user->id,
        ]));

        $response->assertStatus(200)
            ->assertJsonFragment([
                'id' => $user->id,
                'url' => $user->url,
//                'comments' => $photo->comments
//                    ->sortByDesc('id')
//                    ->map(function ($comment) {
//                        return [
//                            'author' => [
//                                'name' => $comment->author->name,
//                            ],
//                            'content' => $comment->content,
//                        ];
//                    })
//                    ->all(),
            ]);
    }
}
