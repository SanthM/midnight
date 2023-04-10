const { WAConnection, MessageType } = require('@adiwajshing/baileys');
const fs = require('fs');

// Crea una nueva conexión
const client = new WAConnection();

// Función para convertir una imagen en un sticker
async function convertirASticker(mensaje) {
  // Obtén la imagen adjunta al mensaje
  const imagen = await client.downloadMediaMessage(mensaje);

  // Convierte la imagen en un sticker
  const sticker = await client.sendMessage(mensaje.from, imagen, {
    mimetype: 'image/png',
    sticker: true
  }, {
    quoted: mensaje
  });

  console.log('Sticker creado:', sticker);
}

// Conecta el cliente a WhatsApp Web
client.connect();

// Cuando la conexión se establece correctamente, muestra un mensaje de confirmación
client.on('open', () => {
  console.log('Conexión establecida');
});

// Escucha los mensajes entrantes
client.on('message', async (mensaje) => {
  // Verifica si el mensaje contiene el comando /sticker
  if (mensaje.body.toLowerCase().includes('/sticker')) {
    // Verifica si el mensaje tiene una imagen adjunta
    if (mensaje.hasMedia && mensaje.type === MessageType.image) {
      // Convierte la imagen en un sticker
      await convertirASticker(mensaje);
    } else {
      // Si no hay una imagen adjunta, responde con un mensaje de error
      await client.sendMessage(mensaje.from, 'Debes adjuntar una imagen para convertirla en sticker.');
    }
  }
});
