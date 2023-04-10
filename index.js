import makeWASocket, { DisconnectReason } from '@adiwajshing/baileys'
import { Boom } from '@hapi/boom'

async function connectToWhatsApp() {
  const sock = makeWASocket({
    // can provide additional config here
    printQRInTerminal: true
  })
  sock.ev.on('connection.update', (update) => {
    const { connection, lastDisconnect } = update
    if (connection === 'close') {
      const shouldReconnect = (lastDisconnect.error as Boom)?.output?.statusCode !== DisconnectReason.loggedOut
      console.log('connection closed due to ', lastDisconnect.error, ', reconnecting ', shouldReconnect)
      // reconnect if not logged out
      if (shouldReconnect) {
        connectToWhatsApp()
      }
    } else if (connection === 'open') {
      console.log('opened connection')
    }
  })
  sock.ev.on('messages.upsert', async m => {
    if (m.messages?.[0]?.message?.imageMessage?.mimetype.startsWith('image/') ||
      m.messages?.[0]?.message?.videoMessage?.mimetype.startsWith('video/')) {
      if (m.messages[0].message.caption === '/sticker') {
        console.log('converting to sticker')
        const buffer = await sock.downloadMediaMessage(m.messages[0])
        const sticker = await sock.sendMessage(m.messages[0].key.remoteJid!, {
          sticker: {
            webpBase64: buffer.toString('base64')
          }
        }, 'stickerMessage')
        console.log('sticker sent')
      }
    }
  })
}

connectToWhatsApp()
