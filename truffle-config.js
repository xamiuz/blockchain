// truffle-config.js

module.exports = {
  // Konfigurasi untuk pengembangan dengan Ganache
  networks: {
    development: {
      host: "127.0.0.1",   // URL host Ganache
      port: 7545,          // Port yang digunakan oleh Ganache
      network_id: "5777",  // ID jaringan Ganache (default)
      gas: 6721975,        // Gas limit
      gasPrice: 20000000000, // Gas price (di sini dalam wei, bisa disesuaikan)
    },
    // Konfigurasi jaringan lainnya bisa ditambahkan di sini
  },

  // Kompiler Solidity
  compilers: {
    solc: {
      version: "0.8.0",    // Versi Solidity yang digunakan
      settings: {
        optimizer: {
          enabled: true,  // Mengaktifkan optimisasi kompilasi
          runs: 200       // Berapa kali optimisasi dijalankan
        }
      }
    }
  },

  // Menambahkan pengaturan untuk Truffle Dashboard atau tools lain
  // plugins: ["truffle-plugin-verify"],

  // Mocha konfigurasi untuk testing
  mocha: {
    // Timeout testing dalam milidetik
    timeout: 100000
  },

  // Pengaturan untuk pengujian dan deployment script
  migrations_directory: "./migrations",  // Folder tempat file migrasi
  contracts_directory: "./contracts",    // Folder tempat kontrak Solidity disimpan
  contracts_build_directory: "./build/contracts",  // Tempat untuk menyimpan kontrak yang telah terkompilasi

  // Pengaturan untuk build dan testing
  test_directory: "./test",  // Folder untuk menempatkan file testing

  // Console Settings
  console: {
    // Mengaktifkan fitur 'console.log' di dalam pengujian (testing)
    log: true
  }
};
