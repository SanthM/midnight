const { create } = require('venom-bot');

create().then((client) => {
  client.onMessage(async (message) => {
    // Detectar si el mensaje contiene un sticker
    if (message?.mimetype === 'image/webp') {
      const caption = message.caption?.toLowerCase() || '';
      if (caption.includes('/sticker')) {
        // Convertir la imagen en un sticker
        const media = await client.decryptMedia(message);
        const sticker = await client.getStickerFromWebp(media);
        await client.sendRawWebpAsSticker(
          message.from,
          sticker,
          {},
          message.id.toString()
        );
      }
    }
  });
});
