/* ============
 * 파이어베이스 에러리스트
 * ============
 */
export default (error) => {
  const err = error;
  let message = '진행중 문제가 발생하였습니다 \n 잠시후 다시 진행하시거나 관리자에게 문의해주세요';

  switch (err.code) {
    // 이메일 로그인 관련
    case 'auth/missing-email':
      message = '이메일을 입력해주세요';
      break;
    case 'auth/invalid-email':
      message = '유효하지 않은 이메일입니다';
      break;
    case 'auth/invalid-email-verified':
      message = '유효하지 않은 이메일입니다';
      break;
    case 'auth/user-not-found':
      message = '존재하지 않는 사용자입니다';
      break;
    case 'auth/wrong-password':
      message = '비밀번호가 일치하지 않습니다';
      break;
    case 'auth/invalid-password':
      message = '유효하지 않은 비밀번호가 입력되었습니다';
      break;
    case 'auth/invalid-password-hash':
      message = '유효하지 않은 비밀번호가 입력되었습니다';
      break;
    case 'auth/invalid-password-salt':
      message = '유효하지 않은 비밀번호가 입력되었습니다';
      break;
    case 'auth/invalid-photo-url':
      message = '업로드한 프로필이미지의 URL이 잘못되었습니다';
      break;
    case 'auth/email-already-exists':
      message = '이미 사용중인 이메일입니다';
      break;
    case 'auth/invalid-display-name':
      message = '표시명이 잘못되었습니다';
      break;
    case 'auth/invalid-credential':
      message = '유효하지 않은 접근입니다';
      break;
    case 'auth/session-cookie-revoked':
      message = '인증시간이 만료되었습니다';
      break;
    case 'auth/session-cookie-expired':
      message = '인증시간이 만료되었습니다';
      break;
    case 'auth/id-token-expired':
      message = '인증시간이 만료되었습니다';
      break;
    case 'auth/id-token-revoked':
      message = '인증시간이 만료되었습니다';
      break;
    case 'auth/requires-recent-login':
      message = '인증정보가 유효하지 않습니다\n 다시 로그인해서 진행해주세요';
      break;
    // 구글로그인 관련
    case 'auth/popup-closed-by-user':
      message = '인증 팝업화면이 닫혔습니다\n 다시 진행해주세요';
      break;
    case 'auth/popup-blocked':
      message = '인증 팝업화면이 외부환경에 의해 차단되었습니다\n 차단된 팝업을 허용해주세요';
      break;
    default:
      break;
  }

  return message;
};