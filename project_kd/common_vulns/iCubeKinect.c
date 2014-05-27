// NOTE: This file will not compile and is for reading only

// The code here verifies the iCubeKinect DVDs have not been
// modified and thus should prevent executing arbitrary code

struct rsa_certificate {
  unsigned int key_id;
  char rsa_signature[1024];
  char metadata[32];
  char content_hash[20];
};

int verify_certificate(struct rsa_certificate cert) {
  char *cert_hash=MD5(cert.metadata + cert.content_hash);
  char *sig_hash=rsa_decrypt(cert.rsa_signature, cert.key_id);

  if (strncmp(cert_hash, sig_hash, MD5_LENGTH) == 0) {
     return RSA_CERT_OK;
  } else {
     return RSA_CERT_BAD;
  }
}

int is_a_valid_dvd() {
  struct rsa_certificate cert = get_dvd_cert();

  if(verify_certificate(cert) == RSA_CERT_BAD) {
    return DVD_BAD;
  } else {
    return DVD_OK;
  }
}
