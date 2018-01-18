---
layout: post
title: 'vnc through SSH: how to control your desktop remotely'
author: jayd
tags:
 - vnc
 - ssh
 - remote desktop
 - linux
share: true
---

I won't go into too much detail in this post, as there are [multiple][1] [guides][2]
that go above and beyond in explaining the behind-the-scenes of tunnelling
VNC connections through SSH. Note that this solution uses TigerVNC's `x0vncserver`
to control the remote X server. Simply use `vncserver` if you want to control
a different X server.

The setup is quite simple, but requires two terminal windows. In the first terminal,
SSH into your remote machine with

<pre class="highlight"><code><b>user@local-machine <span class="nv">$ </span></b>ssh -Y &lt;remote.machine.com&gt; -L 5900:localhost:5900
</code></pre>

and then,

<pre class="highlight"><code><b>remoteuser@remote-machine <span class="nv">$ </span></b> x0vncserver -display :0 -passwordfile ~/.vnc/passwdfile
</code></pre>

Now, in the second terminal on your local machine, you can simply type

<pre class="highlight"><code><b>user@local-machine <span class="nv">$</span></b> vncviewer localhost:5900
</code></pre>

The `-L` flag in the SSH connection sets up port forwarding from the local machine
to the remote machine. In short, all unbound traffic that goes through the specified
port on the local machine is forward to the other port on the remote machine. Here we
choose port 5900 on both machines as it is the default port for `x0vncserver`,
but both can be changed freely.

Make sure to generate a password file for VNC by using `vncpasswd` and pass
it to `x0vncserver` on the `passwordfile` flag. Here we choose the default.

The same method with generic ports would read

<pre class="highlight"><code><b>user@local-machine <span class="nv">$ </span></b>ssh -Y &lt;remote.machine.com&gt; -L &lt;xxxx&gt;:localhost:&lt;yyyy&gt;
<b>remoteuser@remote-machine <span class="nv">$ </span></b> x0vncserver -rfbport &lt;yyyy&gt; -display :0 -passwordfile ~/.vnc/passwdfile
</code></pre>

and

<pre class="highlight"><code><b>user@local-machine <span class="nv">$</span></b> vncviewer localhost:&lt;xxxx&gt;
</code></pre>

Until next time, cheers!

[1]: http://www.cl.cam.ac.uk/research/dtg/attarchive/vnc/sshvnc.html
[2]: https://www.cyberciti.biz/tips/tunneling-vnc-connections-over-ssh-howto.html