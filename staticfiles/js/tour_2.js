if (tourData && Array.isArray(tourData)) {
  const sortedTourInfos = tourData.sort((a, b) => a.order - b.order);
  renderTimeline(sortedTourInfos); // Sıralı veriyi işleme
} else {
  console.error("tourData is not an array or is undefined");
}
let markers = [];

function initMap() {
  const mapCenter = { lat: 41.0578724, lng: 29.0208423 };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: mapCenter,
    disableDefaultUI: false, // Varsayılan tüm UI öğelerini kaldırır (isteğe bağlı).
    fullscreenControl: false, // Tam ekran kontrolünü kaldırır.
    streetViewControl: false, // Street View kontrolünü kaldırır.
    mapTypeControl: false, // Harita tipi değiştirme (uydu/normal) kontrolünü kaldırır.
    mapId: "BOLOGO_MAP",
  });

  tourData.forEach((location) => {
    const url = location.google_maps_url;
    const [latitude, longitude] = url.split("/").find(part => part.startsWith("@")).slice(1).split(",").map(Number);

    if (!latitude || !longitude) {
      console.error(`Coordinates not found in URL: ${url}`);
      return; // Eğer geçerli değilse bir sonraki lokasyona geç
    }
    // Marker oluştur
    const marker = new google.maps.marker.AdvancedMarkerElement({
      map,
      position: { lat: latitude, lng: longitude },
      title: location.place_name,
      content: createCustomIcon(location.order, "#5a56e9"), // Varsayılan renk
      // order: location.order,
    });
    marker.order = location.order;
    
    marker.addListener('click', () => {
      highlightActiveLocation(location.order);
    
      // Timeline'daki ilgili öğeyi bul ve 'active' sınıfını ekle
      const activeTimelineItem = document.querySelector(`.timeline-badge:nth-child(${location.order})`);
      if (activeTimelineItem) {
        activeTimelineItem.classList.add('active');
      }
    
      const timelineItem = document.querySelector(`.timeline-item:nth-child(${location.order})`);
      if (timelineItem) {
        timelineItem.querySelector('.timeline-badge').classList.add('active');
        timelineItem.querySelector('.duration').classList.add('active');
        timelineItem.querySelector('.info').classList.add('active');
    
        // İlgili collapse menüsünü aç
        const collapseMenu = timelineItem.querySelector(`#description-${location.order}`);
        if (collapseMenu) {
          const bootstrapCollapse = new bootstrap.Collapse(collapseMenu, {
            toggle: true,
          });
        }
      }
    });
    markers.push(marker);
  });

  // Kullanıcı Canlı Konumu
  let userMarker = null; // Kullanıcı konumunu temsil eden marker
  let accuracyCircle = null; // Doğruluk alanı çemberi

  if (navigator.geolocation) {
    navigator.geolocation.watchPosition(
      (position) => {
        const userPosition = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };

        // Eğer marker daha önce oluşturulmadıysa, oluştur
        if (!userMarker) {
          userMarker = new google.maps.marker.AdvancedMarkerElement({
            map,
            position: userPosition,
            title: "Your Live Location",
            content: createCustomCircleIcon(),
          });
        
          // // Doğruluk alanı çemberini oluştur
          // accuracyCircle = new google.maps.Circle({
          //   center: userPosition,
          //   radius: position.coords.accuracy, // Doğruluk yarıçapı
          //   map: map,
          //   fillColor: "#4285F4",
          //   fillOpacity: 0.2,
          //   strokeColor: "#4285F4",
          //   strokeOpacity: 0.5,
          //   strokeWeight: 1,
          // });
          // accuracyCircle.setCenter(userPosition);
          smoothBlink(userMarker)
        } else {
          // Marker pozisyonunu güncelle
          userMarker.position = userPosition; // Yeni pozisyonu atıyoruz
          userMarker.geometry = {
            location: new google.maps.LatLng(userPosition.lat, userPosition.lng), // Doğru pozisyon
          };
        
          // // Çemberi güncelle
          // accuracyCircle.setCenter(userPosition); // Yeni merkez
          // accuracyCircle.setRadius(position.coords.accuracy); // Yeni doğruluk yarıçapı
        }
      },
      (error) => {
        console.log("Canlı konum alınamadı:", error);
        console.log("Daha doğru konum almak için ayarlar değiştiriliyor...");
      },
      {
        enableHighAccuracy: true, // Daha doğru konum bilgisi alır
        maximumAge: 0, // Eski konum bilgisini kullanmaz
        timeout: 5000, // Konum alma işlemi için zaman aşımı (ms)
      }
    );
  } else {
    console.error("Geolocation API tarayıcı tarafından desteklenmiyor.");
  }
}

function createCustomCircleIcon() {
  const iconWrapper = document.createElement('div');
  // iconWrapper.style.position = 'center';
  iconWrapper.style.width = '22px'; // Çapı `scale` ile eşleşecek şekilde ayarlandı (8 x 2)
  iconWrapper.style.height = '22px';
  iconWrapper.style.borderRadius = '50%'; // CIRCLE şekli
  iconWrapper.style.backgroundColor = '#4285F4'; // fillColor
  iconWrapper.style.border = '3px solid white'; // strokeColor ve strokeWeight

  return iconWrapper;
}

function smoothBlink(markerElement) {
  let opacity = 1; // Başlangıç opaklığı
  let increasing = false; // Opaklık artış/azalış kontrolü

  setInterval(() => {
    // Opaklık değerini artır veya azalt
    if (increasing) {
      opacity += 0.05; // Opaklık artışı
      if (opacity >= 1) {
        opacity = 1;
        increasing = false; // Azalmaya başla
      }
    } else {
      opacity -= 0.05; // Opaklık azalması
      if (opacity <= 0.7) {
        opacity = 0.7;
        increasing = true; // Artmaya başla
      }
    }

    // Marker'ın HTML içeriğindeki opaklığı güncelle
    const content = markerElement.content; // AdvancedMarkerElement içeriği
    if (content) {
      content.style.opacity = opacity.toString(); // CSS üzerinden opaklık ayarı
    }
  }, 100); // Daha sık çalıştırarak daha yumuşak bir geçiş sağlanır
}

function createCustomIcon(order, color) {
  // Bir div elementi oluştur
  const container = document.createElement('div');
  container.style.position = 'relative';
  container.style.width = '45px';
  container.style.height = '45px';

  // SVG içeriği
  const svgIcon = `
    <svg xmlns="http://www.w3.org/2000/svg" width="45" height="45" viewBox="0 0 24 24" fill="${color}">
      <!-- Pin şekli -->
      <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
      <!-- Order numarası -->
      <text x="12" y="13" fill="white" font-size="8" font-family="Arial" text-anchor="middle" dominant-baseline="middle">${order}</text>
    </svg>
  `;

  // SVG'yi bir DOM elementi olarak ekle
  container.innerHTML = svgIcon;

  return container; // Bir DOM Node döndürüyoruz
}

let playingAudios = [];
let intervalId = null;

function renderTimeline(data) {
  data.forEach(item => {
    const timelineItem = document.createElement('li');
    timelineItem.className = 'timeline-item';

    // Varsayılan duration (eğer ses yolu yoksa)
    let durationText = '0:00';
    let audio = null;

    // Eğer voice_path_EN varsa
    let audioPath = null
    if (item.voice_path) {
      audioPath = item.voice_path.includes("media") 
      ? item.voice_path 
      : "/media/" + item.voice_path;
      audio = new Audio(audioPath);
      audio.addEventListener('loadedmetadata', () => {
        const minutes = Math.floor(audio.duration / 60);
        const seconds = Math.floor(audio.duration % 60);
        durationText = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        timelineItem.querySelector('.duration').innerHTML = `<i class="fa fa-headphones me-2"></i> ${durationText}`;
      });
    }

    timelineItem.innerHTML = `
      <span class="timeline-badge">${item.order}</span>
      <div class="timeline-content">
        <h5>
          ${item.place_name} 
          <button class="btn btn-link p-0 ms-2" data-bs-toggle="collapse" data-bs-target="#description-${item.order}" aria-expanded="false" aria-controls="description-${item.order}" id="descriptions-${item.order}">
              <i class="fa fa-chevron-down"></i>
          </button>
        </h5>
        <span class="info info-icon rounded-circle d-inline-flex align-items-center justify-content-center me-2" onclick="openInfoUrl('${item.info_url}')">
          <i class="fa fa-info"></i>
        </span>
        <span class="duration" id="voice-${item.order}"><i class="fa fa-headphones me-2"></i> ${durationText}</span>
      </div>
      <div class="collapse" id="description-${item.order}" data-bs-parent="#timeline">
        <div class="card card-body border-0 rounded-3 shadow">
          <p class="mt-2 fs-7 fs-md-6 fs-sm-10">${item.description}</p>
        </div>
      </div>
    `;

    timeline.appendChild(timelineItem);
    timelineItem.querySelector('.duration').setAttribute('data-audio-path', audioPath);
    // Voice element click listener
    const voiceElement = timelineItem.querySelector(`#voice-${item.order}`);
    voiceElement.addEventListener('click', () => {
      if (voiceElement.classList.contains('paused')) {
        // Müziği devam ettir
        audio.play();
        voiceElement.innerHTML = `<i class="fa fa-pause me-2"></i> ${durationText}`;
        voiceElement.classList.remove('paused');
        voiceElement.classList.add('listening');
        startLiveUpdate(audio, voiceElement); // Süreyi canlı güncelle
        // Çalan sesleri listeye ekle
        playingAudios.push(audio);

        // Ses bittiğinde listeden kaldır
        audio.addEventListener('ended', () => {
          playingAudios = playingAudios.filter(a => a !== audio);
          voiceElement.innerHTML = `<i class="fa fa-headphones me-2"></i> ${totalDuration}`;
          voiceElement.classList.remove('listening', 'paused');
        });
      } else if (voiceElement.classList.contains('listening')) {
        // Müziği durdur
        audio.pause();
        voiceElement.innerHTML = `<i class="fa fa-play me-2"></i> ${durationText}`;
        voiceElement.classList.remove('listening');
        voiceElement.classList.add('paused');
        stopLiveUpdate(); // Süre güncellemeyi durdur
      } else {
        // Yeni bir şarkı çalmaya başlat
        stopAllAudios(); // Tüm çalan sesleri durdur
        audio.currentTime = 0; // Sıfırdan başlat
        audio.play();
        voiceElement.innerHTML = `<i class="fa fa-pause me-2"></i> ${durationText}`;
        voiceElement.classList.add('listening');
        startLiveUpdate(audio, voiceElement); // Süreyi canlı güncelle
        playingAudios.push(audio);
        // Ses bittiğinde listeden kaldır
        audio.addEventListener('ended', () => {
          playingAudios = playingAudios.filter(a => a !== audio);
          const audioPath = voiceElement.getAttribute('data-audio-path'); // Ses dosyasının yolunu al
          if (audioPath) {
            // Yeni bir Audio nesnesi oluştur ve süresini hesapla
            const tempAudio = new Audio(audioPath);
            tempAudio.addEventListener('loadedmetadata', () => {
              const minutes = Math.floor(tempAudio.duration / 60);
              const seconds = Math.floor(tempAudio.duration % 60);
              const totalDuration = `${minutes}:${seconds.toString().padStart(2, '0')}`;
              voiceElement.innerHTML = `<i class="fa fa-headphones me-2"></i> ${totalDuration}`; // Toplam süreyi göster
            });
          }
          voiceElement.classList.remove('listening', 'paused');
        });
      }
    });

    // Click event for active state
    const activeElement = timelineItem.querySelector(`#descriptions-${item.order}`);
    activeElement.addEventListener('click', () => {
      highlightActiveLocation(item.order);
      // Tüm timeline-badge ve duration elementlerinden 'active' sınıfını kaldır
      document.querySelectorAll('.timeline-item .timeline-badge').forEach(badge => badge.classList.remove('active'));
      document.querySelectorAll('.timeline-item .info').forEach(badge => badge.classList.remove('active'));
      document.querySelectorAll('.timeline-item .duration').forEach(duration => duration.classList.remove('active', 'listening', 'paused'));

      // Çalan tüm sesleri durdur ve sıfırla
      stopAllAudios();

      // Şu anki öğeye 'active' sınıfını ekle
      timelineItem.querySelector('.info').classList.add('active');
      timelineItem.querySelector('.timeline-badge').classList.add('active');
      timelineItem.querySelector('.duration').classList.add('active');
    });
  });
}

function openInfoUrl(url) {
  if (url) {
    window.open(url, '_blank'); // Yeni sekmede açar
  } else {
    console.error('URL is not defined');
  }
}

function stopAllAudios() {
  // Tüm çalan sesleri durdur
  if (playingAudios.length > 0) {
    playingAudios.forEach(audio => {
      if (!audio.paused) {
        audio.pause(); // Sesleri durdur
        audio.currentTime = 0; // Süreyi sıfırla
      }
    });
    playingAudios = []; // Çalan sesler listesini temizle
  }

  // Tüm timeline öğelerinde 'listening' ve 'paused' sınıflarını kaldır
  document.querySelectorAll('.timeline-item .duration').forEach(duration => {
    const audioPath = duration.getAttribute('data-audio-path'); // Ses dosyasının yolunu al
    if (audioPath) {
      // Yeni bir Audio nesnesi oluştur ve süresini hesapla
      const tempAudio = new Audio(audioPath);
      tempAudio.addEventListener('loadedmetadata', () => {
        const minutes = Math.floor(tempAudio.duration / 60);
        const seconds = Math.floor(tempAudio.duration % 60);
        const totalDuration = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        duration.innerHTML = `<i class="fa fa-headphones me-2"></i> ${totalDuration}`; // Toplam süreyi göster
      });
    }
    duration.classList.remove('listening', 'paused'); // Sınıfları kaldır
  });

  // Süre güncellemeyi durdur
  stopLiveUpdate();
}

// Süreyi canlı güncelleme başlat
function startLiveUpdate(audio, element) {
  stopLiveUpdate(); // Mevcut güncellemeyi durdur
  intervalId = setInterval(() => {
    const minutes = Math.floor(audio.currentTime / 60);
    const seconds = Math.floor(audio.currentTime % 60);
    const currentTimeText = `${minutes}:${seconds.toString().padStart(2, '0')}`;
    element.innerHTML = `<i class="fa fa-pause me-2"></i> ${currentTimeText}`;
  }, 1000);
}

// Süreyi canlı güncellemeyi durdur
function stopLiveUpdate() {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
  }
}

function highlightActiveLocation(order) {
  document.querySelectorAll('.timeline-item .timeline-badge').forEach(badge => badge.classList.remove('active'));
  document.querySelectorAll('.timeline-item .duration').forEach(duration => duration.classList.remove('active', 'listening', 'paused'));
  document.querySelectorAll('.timeline-item .info').forEach(badge => badge.classList.remove('active'));
  // Çalan tüm sesleri durdur ve sıfırla
  stopAllAudios();

  // Timeline'da belirtilen order için active sınıfını ekle
  const activeTimelineItem = document.querySelector(`.timeline-item:nth-child(${order})`);
  if (activeTimelineItem) {
    activeTimelineItem.querySelector('.timeline-badge').classList.add('active');
    activeTimelineItem.querySelector('.duration').classList.add('active');
    activeTimelineItem.querySelector('.info').classList.add('active');
    // İlgili öğeye doğru kaydırma sadece timeline-container içinde
    const timelineContainer = document.querySelector('.timeline-container');
    if (timelineContainer) {
      const offsetTop = activeTimelineItem.offsetTop; // Öğenin container içindeki üstten uzaklığı
      const scrollHeight = timelineContainer.scrollTop; // Timeline'ın mevcut kaydırma yüksekliği
      const containerHeight = timelineContainer.clientHeight; // Container'ın yüksekliği

      // Kaydırma ayarları
      timelineContainer.scrollTo({
        top: offsetTop - containerHeight / 4, // Ortalamak için hesaplama
        behavior: 'smooth', // Animasyonlu kaydırma
      });
    }

    // İlgili collapse menüsünü aç
    const collapseMenu = activeTimelineItem.querySelector(`#description-${order}`);
    if (collapseMenu) {
      const bootstrapCollapse = new bootstrap.Collapse(collapseMenu, {
        toggle: true,
      });
    }
  }

  // Haritadaki tüm marker'lardan sarı highlight'ı kaldır
  markers.forEach(marker => {
    marker.content = createCustomIcon(marker.order, "#5a56e9");
  });

  // Belirtilen order için marker'ı sarı yap
  const activeMarker = markers.find(marker => marker.order === order);
  if (activeMarker) {
    activeMarker.content = createCustomIcon(order, "#FF7F00"); // Aktif renk
  }
}