import voucher
from voucher import *  # Vrq, Vch, ATTR_*, ...
from voucher import from_cbor

_voucher = voucher.voucher  # debug


def test_voucher_mbedtls_version():
    from voucher import mbedtls_version

    assert mbedtls_version.version.startswith('mbed TLS 3.')
    assert mbedtls_version.version_info[0] == 3

def test_voucher_version():
    assert voucher.version.startswith('Rust voucher ')

def test_example_usage():
    """
use minerva_voucher::{Voucher, attr::*};

// Create an empty voucher request.
let mut vrq = Voucher::new_vrq();

// Add some attributes.
vrq.set(Attr::Assertion(Assertion::Proximity))
    .set(Attr::CreatedOn(1599086034))
    .set(Attr::SerialNumber(b"00-D0-E5-F2-00-02".to_vec()));

// Count attributes.
assert_eq!(vrq.len(), 3);

// Check for specific ones.
assert_eq!(vrq.get(ATTR_CREATED_ON), Some(&Attr::CreatedOn(1599086034)));
assert_eq!(vrq.get(ATTR_EXPIRES_ON), None);

// Remove a specific one.
assert_eq!(vrq.remove(ATTR_CREATED_ON), true);

// Count attributes again.
assert_eq!(vrq.len(), 2);

// Iterate over everything.
for attr in vrq.iter() {
    println!("attr: {:?}", attr);
}
    """

    # Create an empty voucher request.
    vrq = Vrq()

    # Add some attributes.
    vrq[ATTR_ASSERTION] = ASSERTION_PROXIMITY
    vrq[ATTR_CREATED_ON] = 1599086034
    vrq[ATTR_SERIAL_NUMBER] = '00-D0-E5-F2-00-02'

    # Count attributes.
    assert len(vrq) == 3

    # Check for specific ones.
    assert vrq[ATTR_CREATED_ON] == 1599086034
    assert vrq[ATTR_EXPIRES_ON] == None

    # Remove a specific one.
    assert vrq.remove(ATTR_CREATED_ON) == True

    # Count attributes again.
    assert len(vrq) == 2

    # Iterate over everything.
    for k, v in vrq:
        print(f'vrq[{k}]: {v}')

    # !!!!
    print(vrq)
    #assert 0  # !!!!

import os
VOUCHER_SAMPLE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../voucher/data')

def test_example_cbor_encoding():
    """
use minerva_voucher::{Voucher, attr::*, SignatureAlgorithm, Sign};

static KEY_PEM_F2_00_02: &[u8] = core::include_bytes!(
    concat!(env!("CARGO_MANIFEST_DIR"), "/data/00-D0-E5-F2-00-02/key.pem"));

// This is required when the `Sign` trait is backed by mbedtls.
minerva_voucher::init_psa_crypto();

// Create a voucher request with five attributes and COSE-sign it.
let mut vrq = Voucher::new_vrq();
assert!(vrq
    .set(Attr::Assertion(Assertion::Proximity))
    .set(Attr::CreatedOn(1599086034))
    .set(Attr::Nonce(vec![48, 130, 1, 216, 48, 130, 1, 94, 160, 3, 2, 1, 2, 2, 1, 1, 48, 10, 6, 8, 42, 134, 72, 206, 61, 4, 3, 2, 48, 115, 49, 18, 48, 16, 6, 10, 9, 146, 38, 137, 147, 242, 44, 100, 1, 25, 22, 2, 99, 97, 49, 25, 48, 23, 6, 10, 9, 146, 38, 137, 147, 242, 44, 100, 1, 25, 22, 9, 115, 97, 110, 100, 101, 108, 109, 97, 110, 49, 66, 48, 64, 6, 3, 85, 4, 3, 12, 57, 35, 60, 83, 121, 115, 116, 101, 109, 86, 97, 114, 105, 97, 98, 108, 101, 58, 48, 120, 48, 48, 48, 48, 53, 53, 98, 56, 50, 53, 48, 99, 48, 100, 98, 56, 62, 32, 85, 110, 115, 116, 114, 117, 110, 103, 32, 70, 111, 117, 110, 116, 97, 105, 110, 32, 67, 65, 48, 30, 23, 13, 50, 48, 48, 56, 50, 57, 48, 52, 48, 48, 49, 54, 90, 23, 13, 50, 50, 48, 56, 50, 57, 48, 52, 48, 48, 49, 54, 90, 48, 70, 49, 18, 48, 16, 6, 10, 9, 146, 38, 137, 147, 242, 44, 100, 1, 25, 22, 2, 99, 97, 49, 25, 48, 23, 6, 10, 9, 146, 38, 137, 147, 242, 44, 100, 1, 25, 22, 9, 115, 97, 110, 100, 101, 108, 109, 97, 110, 49, 21, 48, 19, 6, 3, 85, 4, 3, 12, 12, 85, 110, 115, 116, 114, 117, 110, 103, 32, 74, 82, 67, 48, 89, 48, 19, 6, 7, 42, 134, 72, 206, 61, 2, 1, 6, 8, 42, 134, 72, 206, 61, 3, 1, 7, 3, 66, 0, 4, 150, 101, 80, 114, 52, 186, 159, 229, 221, 230, 95, 246, 240, 129, 111, 233, 72, 158, 129, 12, 18, 7, 59, 70, 143, 151, 100, 43, 99, 0, 141, 2, 15, 87, 201, 124, 148, 127, 132, 140, 178, 14, 97, 214, 201, 136, 141, 21, 180, 66, 31, 215, 242, 106, 183, 228, 206, 5, 248, 167, 76, 211, 139, 58, 163, 16, 48, 14, 48, 12, 6, 3, 85, 29, 19, 1, 1, 255, 4, 2, 48, 0, 48, 10, 6, 8, 42, 134, 72, 206, 61, 4, 3, 2, 3, 104, 0, 48, 101, 2, 49, 0, 135, 158, 205, 227, 138, 5, 18, 46, 182, 247, 44, 178, 27, 195, 210, 92, 190, 230, 87, 55, 112, 86, 156, 236, 35, 12, 164, 140, 57, 241, 64, 77, 114, 212, 215, 85, 5, 155, 128, 130, 2, 14, 212, 29, 79, 17, 159, 231, 2, 48, 60, 20, 216, 138, 10, 252, 64, 71, 207, 31, 135, 184, 115, 193, 106, 40, 191, 184, 60, 15, 136, 67, 77, 157, 243, 247, 168, 110, 45, 198, 189, 136, 149, 68, 47, 32, 55, 237, 204, 228, 133, 91, 17, 218, 154, 25, 228, 232]))
    .set(Attr::ProximityRegistrarCert(vec![102, 114, 118, 85, 105, 90, 104, 89, 56, 80, 110, 86, 108, 82, 75, 67, 73, 83, 51, 113, 77, 81]))
    .set(Attr::SerialNumber(b"00-D0-E5-F2-00-02".to_vec()))
    .sign(KEY_PEM_F2_00_02, SignatureAlgorithm::ES256)
    .is_ok());

// Encode the voucher request.
let cbor = vrq.serialize().unwrap();

assert_eq!(cbor.len(), 630);
    """

    KEY_PEM_F2_00_02 = open(os.path.join(VOUCHER_SAMPLE_DIR, '00-D0-E5-F2-00-02/key.pem'), 'rb').read()

    # Create a voucher request with five attributes and COSE-sign it.
    vrq = Vrq()
    vrq[ATTR_ASSERTION] = ASSERTION_PROXIMITY
    vrq[ATTR_CREATED_ON] = 1599086034
    vrq[ATTR_NONCE] = bytes([48, 130, 1, 216, 48, 130, 1, 94, 160, 3, 2, 1, 2, 2, 1, 1, 48, 10, 6, 8, 42, 134, 72, 206, 61, 4, 3, 2, 48, 115, 49, 18, 48, 16, 6, 10, 9, 146, 38, 137, 147, 242, 44, 100, 1, 25, 22, 2, 99, 97, 49, 25, 48, 23, 6, 10, 9, 146, 38, 137, 147, 242, 44, 100, 1, 25, 22, 9, 115, 97, 110, 100, 101, 108, 109, 97, 110, 49, 66, 48, 64, 6, 3, 85, 4, 3, 12, 57, 35, 60, 83, 121, 115, 116, 101, 109, 86, 97, 114, 105, 97, 98, 108, 101, 58, 48, 120, 48, 48, 48, 48, 53, 53, 98, 56, 50, 53, 48, 99, 48, 100, 98, 56, 62, 32, 85, 110, 115, 116, 114, 117, 110, 103, 32, 70, 111, 117, 110, 116, 97, 105, 110, 32, 67, 65, 48, 30, 23, 13, 50, 48, 48, 56, 50, 57, 48, 52, 48, 48, 49, 54, 90, 23, 13, 50, 50, 48, 56, 50, 57, 48, 52, 48, 48, 49, 54, 90, 48, 70, 49, 18, 48, 16, 6, 10, 9, 146, 38, 137, 147, 242, 44, 100, 1, 25, 22, 2, 99, 97, 49, 25, 48, 23, 6, 10, 9, 146, 38, 137, 147, 242, 44, 100, 1, 25, 22, 9, 115, 97, 110, 100, 101, 108, 109, 97, 110, 49, 21, 48, 19, 6, 3, 85, 4, 3, 12, 12, 85, 110, 115, 116, 114, 117, 110, 103, 32, 74, 82, 67, 48, 89, 48, 19, 6, 7, 42, 134, 72, 206, 61, 2, 1, 6, 8, 42, 134, 72, 206, 61, 3, 1, 7, 3, 66, 0, 4, 150, 101, 80, 114, 52, 186, 159, 229, 221, 230, 95, 246, 240, 129, 111, 233, 72, 158, 129, 12, 18, 7, 59, 70, 143, 151, 100, 43, 99, 0, 141, 2, 15, 87, 201, 124, 148, 127, 132, 140, 178, 14, 97, 214, 201, 136, 141, 21, 180, 66, 31, 215, 242, 106, 183, 228, 206, 5, 248, 167, 76, 211, 139, 58, 163, 16, 48, 14, 48, 12, 6, 3, 85, 29, 19, 1, 1, 255, 4, 2, 48, 0, 48, 10, 6, 8, 42, 134, 72, 206, 61, 4, 3, 2, 3, 104, 0, 48, 101, 2, 49, 0, 135, 158, 205, 227, 138, 5, 18, 46, 182, 247, 44, 178, 27, 195, 210, 92, 190, 230, 87, 55, 112, 86, 156, 236, 35, 12, 164, 140, 57, 241, 64, 77, 114, 212, 215, 85, 5, 155, 128, 130, 2, 14, 212, 29, 79, 17, 159, 231, 2, 48, 60, 20, 216, 138, 10, 252, 64, 71, 207, 31, 135, 184, 115, 193, 106, 40, 191, 184, 60, 15, 136, 67, 77, 157, 243, 247, 168, 110, 45, 198, 189, 136, 149, 68, 47, 32, 55, 237, 204, 228, 133, 91, 17, 218, 154, 25, 228, 232])
    vrq[ATTR_PROXIMITY_REGISTRAR_CERT] = bytes([102, 114, 118, 85, 105, 90, 104, 89, 56, 80, 110, 86, 108, 82, 75, 67, 73, 83, 51, 113, 77, 81])
    vrq[ATTR_SERIAL_NUMBER] = '00-D0-E5-F2-00-02'
    vrq.sign(KEY_PEM_F2_00_02, SA_ES256)

    # Encode the voucher request.
    cbor = vrq.to_cbor()

    assert len(cbor) == 630


def test_example_cbor_decoding():
    """
use minerva_voucher::{Voucher, attr::*, Validate};
use core::convert::TryFrom;

static VCH_F2_00_02: &[u8] = core::include_bytes!(
    concat!(env!("CARGO_MANIFEST_DIR"), "/data/00-D0-E5-F2-00-02/voucher_00-D0-E5-F2-00-02.vch"));
static MASA_CRT_F2_00_02: &[u8] = core::include_bytes!(
    concat!(env!("CARGO_MANIFEST_DIR"), "/data/00-D0-E5-F2-00-02/masa.crt"));

// This is required when the `Validate` trait is backed by mbedtls.
minerva_voucher::init_psa_crypto();

// Decode the voucher.
let vch = Voucher::try_from(VCH_F2_00_02).unwrap();

// COSE-validate the voucher.
assert!(vch.validate(Some(MASA_CRT_F2_00_02)).is_ok());

// This voucher has five attributes.
assert_eq!(vch.len(), 5);

for attr in vch.iter() {
    println!("attr: {:?}", attr);

    // Check data belonging to the attribute.
    match attr {
        Attr::Assertion(x) => assert_eq!(x, &Assertion::Logged),
        Attr::CreatedOn(x) => assert_eq!(x, &1599525239),
        Attr::Nonce(x) => assert_eq!(x, &[88, 83, 121, 70, 52, 76, 76, 73, 105, 113, 85, 50, 45, 79, 71, 107, 54, 108, 70, 67, 65, 103]),
        Attr::PinnedDomainCert(x) => assert_eq!(x[0..4], [77, 73, 73, 66]),
        Attr::SerialNumber(x) => assert_eq!(x, b"00-D0-E5-F2-00-02"),
        _ => panic!(),
    }
}
    """

    VCH_F2_00_02 = open(os.path.join(VOUCHER_SAMPLE_DIR, '00-D0-E5-F2-00-02/voucher_00-D0-E5-F2-00-02.vch'), 'rb').read()
    MASA_CRT_F2_00_02 = open(os.path.join(VOUCHER_SAMPLE_DIR, '00-D0-E5-F2-00-02/masa.crt'), 'rb').read()

    # Decode the voucher.
    vch = from_cbor(VCH_F2_00_02)

    # COSE-validate the voucher.
    assert vch.validate(MASA_CRT_F2_00_02)

    # This voucher has five attributes.
    assert len(vch) == 5

    for k, v in vch:
        print(f'vch[{k}] = {v}')

        # Check data belonging to the attribute.
        if k == ATTR_ASSERTION:
            assert v == ASSERTION_LOGGED
        elif k == ATTR_CREATED_ON:
            assert v == 1599525239
        elif k == ATTR_NONCE:
            assert v == bytes([88, 83, 121, 70, 52, 76, 76, 73, 105, 113, 85, 50, 45, 79, 71, 107, 54, 108, 70, 67, 65, 103])
        elif k == ATTR_PINNED_DOMAIN_CERT:
            assert v[0:4] == bytes([77, 73, 73, 66])
        elif k == ATTR_SERIAL_NUMBER:
            assert v == b'00-D0-E5-F2-00-02'
        else:
            assert False


if 0:  # !!!! content of test_sample.py - https://docs.pytest.org/en/7.1.x/getting-started.html
    def func(x):
        return x + 1


    def test_answer():
        assert func(3) == 4


    class TestClass:
        def test_one(self):
            x = "this"
            assert "h" in x

        def test_two(self):
            x = "hello"
            assert hasattr(x, "check")