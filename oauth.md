소셜 로그인(OAuth - 인증 체계)

OAuth 2.0

auth

- authentication(인증 - 로그인)
- authorization(권한 - 로그인 이후)

```
1. 사용자가 카카오링크(/accounts/kakao/login/)
2. 사용자는 카카오 사이트 로그인 페이지를 확인
3. 사용자는 로그인 정보를 카카오로 보냄
4. 카카오는 redirect url로 django 서버로 사용자 토큰을 보냄
5. 해당 토큰을 이용하여 카카오에 인증 요청
6. 카카오에서 확인
7. 로그인
----------------------------------------------
토큰(access token)은 보통 유효기간이 있는데.
refresh token을 통해서 토큰 재발급을 받을 수 있다.
```

```
카카오 - 리소스 서버/인증 서버
사용자 - 유저
django - 클라이언트
```

