#!/usr/bin/env bash

# feel free to modify the following values

share="smb://192.168.0.10/public"
domain="workgroup"
user="username"
pass="password"

# don't touch the following lines

loginfile="/tmp/login.data"

echo $user > $loginfile
echo $domain >> $loginfile
echo $pass >> $loginfile

gio mount $share < $loginfile

rm $loginfile
