<?php

namespace App;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    protected $keyType = 'string';

    public $timestamps = false;

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'id', 'follower_total', 'url', 'icon', 'bio', 'checked'
    ];

    protected $visible = [
        'id', 'follower_total', 'url', 'icon', 'bio', 'checked',
        'followers_count', 'followings_count'
    ];

    protected $appends = [
        'followers_count', 'followings_count'
    ];

    protected $hidden = [
        'password', 'remember_token',
    ];

    /**
     * The attributes that should be cast to native types.
     *
     * @var array
     */
//    protected $casts = [
//        'email_verified_at' => 'datetime',
//    ];
    /**
     * リレーションシップ - followers
     * @return \Illuminate\Database\Eloquent\Relations\BelongsToMany
     */
    public function followers()
    {
        return $this->belongsToMany('App\User', 'follows', 'follow_to', 'follow_by');
    }

    /**
     * リレーションシップ - followings
     * @return \Illuminate\Database\Eloquent\Relations\BelongsToMany
     */
    public function followings()
    {
        return $this->belongsToMany('App\User', 'follows', 'follow_by', 'follow_to');
    }

    /**
     * アクセサ - followers_count
     * @return int
     */
    public function getFollowersCountAttribute()
    {
        return $this->followers()->count();
    }

    /**
     * アクセサ - followings_count
     * @return int
     */
    public function getFollowingsCountAttribute()
    {
        return $this->followings()->count();
    }
}
