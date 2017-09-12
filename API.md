API
===
## main Mumble object
&gt; class Mumble(host, user, port=64738, password='', certfile=None, keyfile=None, reconnect=False, tokens=[], debug=False)

It should be quite straightforward. `debug=True` will generate a LOT of stdout messages. Otherwise it should be silent in normal conditions.
Reconnect should allow the library to reconnect automatically if the server disconnect it.

The `tokens` parameter is a list of tokens for the channels access tokens

&gt; Mumble.start()

Start the library thread and the connection process

&gt; Mumble.is_ready()

Block until the connection process is concluded.

&gt; Mumble.set_bandwidth(int)

Set (in bit per seconds) the allowed total outgoing bandwidth of the library. Can be limited by the server.

&gt; Mumble.set_application_string(string)

Set the application name that will be sent to the server. Must be done before the `start()`.

&gt; Mumble.set_loop_rate(float)

Set in second how long the library will wait for an incoming message, which slowdown the loop.
Must be small enough for the audio treatment you need, but if too small it will consume too much CPU
0.01 is the default and seems to be small enough to send audio in 20ms packets.
For application that just receive sound, bigger should be enough (like 0.05).

&gt; Mumble.get_loop_rate()

Return the current `loop_rate`.

&gt; Mumble.set_receive_sound(bool)

By default, incoming sound is not treated. If you plan to use the incoming audio, you must set this to `True`,
but then you have to get the audio out of the library regularly otherwise it will simply consume memory.

## Callbacks object (accessible through Mumble.callbacks)
Manage the different available callbacks.
It is basically a `dict` of the available callbacks and the methods to manage them.

Callback names are in `pymumble.constants` module, starting with `PYMUMBLE_CLBK_`
- `PYMUMBLE_CLBK_CONNECTED`: connection succeeded
- `PYMUMBLE_CLBK_CHANNELCREATED`: send the created channel object as parameter
- `PYMUMBLE_CLBK_CHANNELUPDATED`: send the updated channel object and a dict with all the modified fields as parameter
- `PYMUMBLE_CLBK_CHANNELREMOVED`: send the removed channel object as parameter
- `PYMUMBLE_CLBK_USERCREATED`: send the added user object as parameter
- `PYMUMBLE_CLBK_USERUPDATED`: send the updated user object and a dict with all the modified fields as parameter
- `PYMUMBLE_CLBK_USERREMOVED`: send the removed user object and the mumble message as parameter
- `PYMUMBLE_CLBK_SOUNDRECEIVED`: send the user object that received the sound and the SoundChunk object itself
- `PYMUMBLE_CLBK_TEXTMESSAGERECEIVED`: send the received message

*Callbacks are executed within the library looping thread. Keep it's work short or you could have jitter issues!*

&gt; Mumble.callbacks.set_callback(callback, function)

Assign a function to a callback (replace the previous ones if any).

&gt; Mumble.callbacks.add_callback(callback, function)

Assign an additional function to a callback.

&gt; Mumble.callbacks.get_callback(callback)

Return a list of functions assign to this callback or `None`.

&gt; Mumble.callbacks.remove_callback(callback, function)

Remove the specified function from the ones assign to this callback.

&gt; Mumble.callbacks.reset_callback(callback)

Remove all defined callback functions for this callback.

&gt; Mumble.callbacks.get_callbacks_list()

Return the list of all the available callbacks. Better use the constants though.

## Users object (accessible through Mumble.users)
Store the users connected on the server. For the application, it is basically only interesting as a `dict` of `User` objects,
which contain the actual information.

&gt; Mumble.users[int]

Where `int` is the session number on the server. It points to the specific `User` object for this session.

&gt; Mumble.users.count()

Return the number of connected users on the server.

&gt; Mumble.users.myself_session

Contain the session number of the `pymumble` connection itself.

&gt; Mumble.users.myself

Is a shortcut to `Mumble.users[Mumble.users.myself_session]`, pointing to the User object of the current connection.

## User object (accessible through Mumble.users[session] or Mumble.users.myself
Contain the users information and method to act on them.
User also contain an instance of the SoundQueue object, containing the audio received from this user.

&gt; User.sound

SoundQueue instance for this user.

&gt; User.get_property()

Return the value of the property.

&gt; User.mute()
&gt; User.unmute()

&gt; User.deafen()
&gt; User.undeafen()

&gt; User.suppress()
&gt; User.unsuppress()

&gt; User.recording()
&gt; User.unrecorfing()

&gt; User.comment(string)

Set the comment for this user.

&gt; user.texture(texture)

Set the image for this user (must be a format recognized by the Mumble clients. PNG seems to work, I had issues with SVG).

&gt; user.send_message(message)

Send a message to the specific user.

## SoundQueue object (accessible through User.sound)
Contains the audio received from a specific user.
Take care of the decoding and keep track on the timing of the reception.

&gt; User.sound.set_receive_sound(bool)

Allow stopping treating incoming audio for a specific user if `False`. `True` by default.

&gt; User.sound.is_sound()

Return `True` if sound is present in this `SoundQueue`.

&gt; User.sound.get_sound(duration=None)

Return a `SoundChunk` object containing the audio received in one packet coming from the server, and discard it from the list.
If `duration` (in sec) is specified and smaller than the size of the next available audio, the split is taken care of.
**DO NOT USE A NON 10ms MULTIPLE AS IT IS THE BASIC UNIT IN MUMBLE.**

&gt; User.sound.first_sound()

Return a `SoundChunk` object (the next one) but do not discard it.
Useful to check it's timing without actually treat it yet.

## SoundChunk object (received from User.sound)
It contains a sound unit, as received from the server.
It as several properties
&gt; SoundChunk.pcm

The PCM buffer for this sound, in 16 bits signed mono little-endian 48000Hz format.

&gt; SoundChunk.timestamp

Time when the packet was received.

&gt; SoundChunk.time

Time calculated based on Mumble sequences (better to reconstruct the stream).

&gt; SoundChunk.sequence

Mumble sequence for the packet.

&gt; SoundChunk.size

Size of the PCM in bytes.

&gt; SoundChunk.duration

Length of the PCM in secs.

&gt; SoundChunk.type

Mumble type for the chunk (coded used).

&gt; SoundChunk.target

Target of the packet, as sent by the server.

## Channels object (accessible through Mumble.channels)
Contains the channels known on the server. Allow listing and finding them.
It is again a `dict` by channel ids (root=0) containing all the Channel objects.

&gt; Mumble.channels.find_by_tree(iterable)

Search, starting from the root for every element a subchannel with the same name.
Return the channel object or raise a `UnknownChannelError` exception.

&gt; Mumble.channels.get_childs(channel_id)

Return a list of all the children objects for a channel id.

&gt; Mumble.channels.get_descendants(channel_id)

Return a (nested) list of the channels above this id.

&gt; Mumble.get_tree(channel_id)

Return a nested list of the channel objects above this id.

&gt; Mumble.find_by_name(name)

Return the first channel object matching the name.

## Channel object (accessible through Mumble.channels[channel_id])
Contains the properties of the specific channel.
Allow to move a user into it.

&gt; Channel.get_property(name)

Return the property value for this channel.

&gt; Channel.move_in(session=None)

Move (or try to) a user's session into the channel.
If no session specified, try to move the library application itself.

&gt; Channel.send_message(message)

Send message into the specific channel.

## SoundOutput object (accessible through Mumble.sound_output)
Takes care of encoding, packetizing and sending the audio to the server.

&gt; Mumble.sound_output.set_audio_per_packet(float)

Set the duration of one packet of audio in secs. Typically, 0.02 or 0.04. Max is 0.12 (codec limitations).

&gt; Mumble.sound_output.get_audio_per_packet()

Return the current length of an audio packet in secs.

&gt; Mumble.sound_output.add_sound(string)

Add PCM sound (16 bites mono 48000Hz little-endian encoded) to the outgoing queue.

&gt; Mumble.sound_output.get_buffer_size()

Return in secs the size of the unsent audio buffer. Useful to transfer audio to the library at a regular pace.
