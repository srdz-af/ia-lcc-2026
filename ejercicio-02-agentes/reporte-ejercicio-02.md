# Reporte Ejercicio 2 - Descripción PEAS de agentes inteligentes

## 1. Asistente virtual de voz

- **Performance:** Maximizar la tasa de comandos comprendidos y ejecutados correctamente, reducir el tiempo de respuesta y evitar acciones no autorizadas.
- **Environment:** Parcialmente observable, estocástico, secuencial y dinámico. Opera en una vivienda o dispositivo conectado, con ruido, usuarios y servicios externos que pueden cambiar.
- **Actuators:** Responder con voz o texto, controlar dispositivos domóticos, crear recordatorios, reproducir contenido y consultar servicios web.
- **Sensors:** Micrófono, texto introducido por el usuario, historial de diálogo, hora, ubicación autorizada y respuestas de APIs conectadas.

## 2. Robot aspirador doméstico

- **Performance:** Maximizar el porcentaje de piso limpio, reducir el tiempo y el consumo de batería, y evitar choques, caídas y atascos.
- **Environment:** Parcialmente observable, estocástico, secuencial, dinámico y continuo. Incluye habitaciones, muebles, escaleras, suciedad, personas y mascotas.
- **Actuators:** Avanzar, retroceder, girar, activar la aspiración y los cepillos, regresar a la base y emitir alertas.
- **Sensors:** Encoders de ruedas, sensor de choque, sensores de caída, sensor de suciedad, cámara o LiDAR, sensor de batería y sensores de distancia.

## 3. Sistema de recomendación de streaming

- **Performance:** Aumentar la satisfacción, la reproducción completa y la retención, reduciendo recomendaciones irrelevantes y el tiempo hasta encontrar contenido.
- **Environment:** Parcialmente observable, estocástico, secuencial, dinámico y principalmente discreto. Incluye catálogo, usuarios, disponibilidad regional y preferencias que cambian con el tiempo.
- **Actuators:** Ordenar el catálogo, generar listas, mostrar trailers, enviar notificaciones y adaptar la página de inicio.
- **Sensors:** Historial de reproducción, búsquedas, pausas, avances, abandonos, calificaciones, dispositivo, hora y características del contenido.

## 4. Vehículo autónomo en ciudad

- **Performance:** Llegar al destino con seguridad, respetar las leyes de tránsito, reducir tiempo y consumo, y mantener la comodidad del pasajero.
- **Environment:** Parcialmente observable, estocástico, secuencial, dinámico y continuo. Incluye tráfico, peatones, ciclistas, semáforos, clima, obras y vehículos con otros objetivos.
- **Actuators:** Girar el volante, acelerar, frenar, cambiar de carril, activar direccionales, luces y claxon.
- **Sensors:** Cámaras, radar o LiDAR, GPS, mapas, IMU, velocímetro, sensores de proximidad y estado del vehículo.

## 5. Agente de trading algorítmico

- **Performance:** Maximizar el rendimiento ajustado al riesgo, limitar pérdidas, controlar costos de transacción y cumplir restricciones de capital.
- **Environment:** Parcialmente observable, estocástico, secuencial, dinámico y continuo. Opera en mercados financieros con otros agentes, noticias y cambios rápidos de liquidez.
- **Actuators:** Comprar, vender, mantener posiciones, cancelar órdenes y modificar límites de precio o volumen.
- **Sensors:** Cotizaciones y volumen en tiempo real, libro de órdenes, historial de precios, noticias, indicadores, saldo y posiciones abiertas.

## 6. Sistema de diagnóstico médico asistido por IA

- **Performance:** Maximizar sensibilidad y especificidad, reducir falsos negativos y falsos positivos, priorizar casos urgentes y entregar resultados a tiempo.
- **Environment:** Parcialmente observable, estocástico, secuencial, dinámico y mixto. El sistema trabaja en un hospital con pacientes, expedientes incompletos y decisiones de médicos.
- **Actuators:** Generar una evaluación, señalar hallazgos, sugerir diagnósticos diferenciales, recomendar estudios y mostrar alertas al médico.
- **Sensors:** Síntomas introducidos, historia clínica, signos vitales, resultados de laboratorio, imágenes clínicas y notas médicas.

## 7. Dron de inspección de infraestructura

- **Performance:** Maximizar la cobertura y la precisión de detección de grietas, corrosión o fugas, minimizando tiempo, consumo y riesgo de colisión.
- **Environment:** Parcialmente observable, estocástico, secuencial, dinámico y continuo. Incluye puentes, tuberías o líneas eléctricas, viento, obstáculos, lluvia y zonas de acceso restringido.
- **Actuators:** Controlar empuje, altitud, dirección y orientación; ajustar la cámara; tomar fotografías; grabar video y regresar al punto de despegue.
- **Sensors:** Cámara de alta resolución, cámara térmica, GPS, IMU, altímetro, LiDAR o sensor de distancia, batería y telemetría.

## 8. Agente jugador de ajedrez

- **Performance:** Maximizar la probabilidad de ganar, evitar perder material o la partida, y respetar el tiempo disponible del reloj.
- **Environment:** Totalmente observable, determinista, secuencial, estático durante el turno, discreto y multiagente. El oponente modifica el estado después de cada jugada.
- **Actuators:** Elegir y ejecutar una jugada legal, ofrecer tablas, abandonar o mostrar análisis y advertencias al usuario.
- **Sensors:** Posición completa del tablero, historial de jugadas, reglas, reloj y jugada realizada por el oponente.
