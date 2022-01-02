# !/usr/bin/env python
# coding:utf-8

import platform
from smb.SMBConnection import SMBConnection

if __name__ == "__main__":

    # connection open
    conn = SMBConnection(
        '', #user
        '', #password
        platform.uname().node,
        '', #remote_hostname
        domain='',
        use_ntlm_v2=True)
    conn.connect('', 139) #ipadd
    print(conn.echo('echo success'))
    files_summary = {}
    
    svc_name = "raspberry_pi"
    remote_path = "music"
    music_folder = conn.listPath(svc_name, remote_path)
    for item in music_folder:
        artist=item.filename
        if '.' in artist:
            continue
        artist_folder = conn.listPath(svc_name, remote_path+'/'+artist)
        print('artist:',artist)
        for item in artist_folder:
            music_album=item.filename
            if '.' in music_album:
                continue
            print(music_album)
            music_album_folder = conn.listPath(svc_name, remote_path+'/'+artist+'/'+music_album)
            for item in music_album_folder:
                music_name=item.filename
                print('music name:',music_name)

    conn.close()