
import BaseApi from './BaseApi';

class PostApi extends BaseApi {
  /**
   * The constructor for the ArtistApi.
   *
   * @param {Object} parameters The query parameters.
   */
  constructor(parameters = {}) {
    // BaseApi.js의 부모의 constructor를 실행, 부모의 endpoint는 reclist사용
    super('post', parameters);
  }

  /**
   * 게시물 가져오기
   */
  getPosts() {
    return this.all();
  }

  /**
   * 게시물 가져오기
   *
   * @param {String} postId 게시물 번호
   *
   * @returns {Promise} The result in a promise.
   */
  getPostDetail(postId) {
    return this.find(postId);
  }

  /**
   * 게시물의 사용자 일정 변경
   *
   * @param {String} sort 정렬
   *
   * @returns {Promise} The result in a promise.
   */
  updatePostCalendar(param) {
    return this.submit('put', `${this.endpoint}/update/post-date`, param);
  }

  /**
   * 게시물 등록
   *
   * @returns {Promise} The result in a promise.
   */
  createPost(param) {
    return this.create(param);
  }

  /**
   * 게시물 수정
   *
   * @returns {Promise} The result in a promise.
   */
  updatePost(param) {
    return this.update(null, param);
  }
}

export default PostApi;